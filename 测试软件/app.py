import os
import json
import requests
import threading
import re
import uuid
import sys
import logging
import unicodedata
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

_log_configured = False

def get_logger():
    global _log_configured
    if not _log_configured:
        _log_configured = True
        log_file = os.path.join(os.path.dirname(__file__), "debug.log")
        try:
            logging.basicConfig(
                filename=log_file,
                level=logging.DEBUG,
                format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s",
                encoding="utf-8",
            )
        except Exception:
            import sys
            print(f"Warning: failed to configure log file: {log_file}", file=sys.stderr)
    return logging.getLogger(__name__)

def log_debug(msg):
    get_logger().debug(msg)

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

app = Flask(__name__, static_folder="static")
_cors_origins_env = os.environ.get("CORS_ORIGINS", "")
if _cors_origins_env:
    _cors_origins = [o.strip() for o in _cors_origins_env.split(",")]
else:
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as _f:
            _cfg = json.load(_f)
    except Exception:
        _cfg = {}
    _cors_origins = _cfg.get("allowed_origins", ["http://localhost:5000", "http://127.0.0.1:5000"])
CORS(app, origins=_cors_origins)


@app.route("/")
def index():
    return app.send_static_file("index.html")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

config_lock = threading.Lock()
stop_generation = 0
stop_lock = threading.Lock()

default_config = {
    "api_key": "",
    "base_url": "",
    "model": "",
    "temperature": 0.7,
    "top_p": 1.0,
    "top_k": 40,
    "min_p": 0.05,
    "context_size": 8192,
    "concurrency": 1,
    "test_count": 1,
    "max_retries": 3,
    "streaming": True,
    "test_set_dir": "",
    "timeout": 60,
    "auto_append_v1": True,
    "allowed_origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
}

config = dict(default_config)


def load_config():
    global config
    try:
        saved = load_json(CONFIG_FILE)
    except Exception as e:
        log_debug(f"加载配置失败: {e}")
        saved = None
    if saved:
        with config_lock:
            config.update(saved)
    else:
        log_debug("未找到有效配置文件，使用默认配置")


def save_config():
    save_json(CONFIG_FILE, config)


def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError, ValueError):
            return None
    return None


def save_json(filepath, data):
    tmppath = filepath + ".tmp"
    try:
        with open(tmppath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmppath, filepath)
    except Exception:
        try:
            if os.path.exists(tmppath):
                os.remove(tmppath)
        except OSError:
            pass
        raise


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def read_file(filepath):
    if os.path.exists(filepath):
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            log_debug(f"文件过大，跳过读取: {filepath}")
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except (UnicodeDecodeError, IOError, OSError):
            return None
    return None


def get_test_set_dir():
    with config_lock:
        d = config.get("test_set_dir")
    if d:
        if os.path.isabs(d):
            return d
        return os.path.normpath(os.path.join(BASE_DIR, d))
    return DATA_DIR


def resolve_test_set_path(*subdirs):
    raw = get_test_set_dir()
    result = os.path.join(raw, *subdirs)
    return unicodedata.normalize("NFKC", result)

def validate_test_set_name(name):
    if not name:
        return False
    name = unicodedata.normalize("NFKC", name)
    if ".." in name or "/" in name or "\\" in name:
        return False
    if name != os.path.basename(name):
        return False
    resolved = os.path.abspath(os.path.join(get_test_set_dir(), name))
    if not resolved.startswith(os.path.abspath(get_test_set_dir())):
        return False
    if sys.platform == "win32":
        reserved = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
                     "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3",
                     "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}
        base = os.path.splitext(name)[0].upper()
        if base in reserved:
            return False
    return True


def validate_file_name(name):
    if not name or len(name) > 255:
        return False
    name = name.strip()
    if not re.match(r'^[\w\u4e00-\u9fff\u3400-\u4dbf\-\.\(\)（） ]+$', name):
        return False
    if name.startswith('.') or name.startswith('_'):
        return False
    return True

# ============ Config ============

@app.route("/api/v1/config", methods=["GET", "POST"])
def handle_config():
    global config
    if request.method == "GET":
        with config_lock:
            return jsonify(config)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "请求体必须为JSON格式"}), 400
    allowed_keys = {"api_key", "base_url", "model", "temperature", "top_p",
                    "top_k", "min_p", "context_size", "concurrency", "test_count",
                    "max_retries", "timeout", "streaming", "test_set_dir", "models",
                    "auto_append_v1"}
    numeric_ranges = {
        "temperature": (0.0, 2.0),
        "top_p": (0.0, 1.0),
        "min_p": (0.0, 1.0),
        "top_k": (0, 200),
        "concurrency": (1, 50),
        "test_count": (1, 100),
        "max_retries": (0, 10),
        "timeout": (5, 600),
        "context_size": (0, 131072),
    }
    warnings_list = []
    with config_lock:
        for k, v in data.items():
            if k not in allowed_keys:
                continue
            if k in numeric_ranges:
                if not isinstance(v, (int, float)):
                    warnings_list.append(f"{k} 值类型无效")
                    continue
                lo, hi = numeric_ranges[k]
                if v < lo or v > hi:
                    warnings_list.append(f"{k} 值 {v} 超出范围 [{lo}, {hi}]，已忽略")
                    continue
            if k == "models" and v is not None and not isinstance(v, list):
                warnings_list.append("models 字段类型无效，应为数组")
                continue
            config[k] = v
        save_config()
    result = {"status": "ok"}
    if warnings_list:
        result["warnings"] = warnings_list
    return jsonify(result)


# ============ Models ============

@app.route("/api/v1/models", methods=["GET", "POST"])
def get_models():
    with config_lock:
        cfg_api_key = config.get("api_key")
        cfg_base_url = config.get("base_url")
    api_key = cfg_api_key

    if not cfg_base_url:
        return jsonify({"error": "Base URL未配置，请在设置中填写API地址"}), 400

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    headers["Content-Type"] = "application/json"

    try:
        response = requests.get(
            f"{cfg_base_url}/models", headers=headers, timeout=30
        )
        if response.status_code == 200:
            models = response.json().get("data", [])
            model_list = [
                {"id": m["id"], "owned_by": m.get("owned_by", "")} for m in models
            ]
            return jsonify(model_list)
        else:
            return jsonify(
                {"error": f"Failed to get models: {response.text}"}
            ), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============ Test Set API ============

@app.route("/api/v1/test-set/scan", methods=["GET"])
def scan_test_sets():
    root = get_test_set_dir()
    if not os.path.exists(root):
        return jsonify({"test_sets": []})
    test_sets = []
    for entry in sorted(os.listdir(root)):
        entry_path = os.path.join(root, entry)
        if os.path.isdir(entry_path) and not entry.startswith("."):
            prompts_dir = os.path.join(entry_path, "测试系统提示词")
            questions_dir = os.path.join(entry_path, "测试问题")
            has_prompts = os.path.exists(prompts_dir)
            has_questions = os.path.exists(questions_dir)
            test_sets.append({
                "name": entry,
                "has_prompts": has_prompts,
                "has_questions": has_questions,
            })
    return jsonify({"test_sets": test_sets})


@app.route("/api/v1/test-set/prompts", methods=["GET"])
def get_test_set_prompts():
    test_set = request.args.get("test_set", "")
    if not test_set:
        return jsonify({"error": "Missing test_set parameter"}), 400
    if not validate_test_set_name(test_set):
        return jsonify({"error": "Invalid test_set name"}), 400
    prompts_dir = resolve_test_set_path(test_set, "测试系统提示词")
    if not os.path.exists(prompts_dir):
        return jsonify({"prompts": [], "warnings": ["目录不存在: 测试系统提示词/"]})
    prompts = []
    warnings = []
    txt_files = {}
    for f in os.listdir(prompts_dir):
        if f.endswith(".txt"):
            if not validate_file_name(f):
                warnings.append(f"文件名不合法，已跳过: {f}")
                continue
            base = f[:-4]
            txt_files[base] = os.path.join(prompts_dir, f)
    for f in sorted(os.listdir(prompts_dir)):
        if not f.endswith(".json"):
            continue
        if not validate_file_name(f):
            warnings.append(f"文件名不合法，已跳过: {f}")
            continue
        base = f[:-5]
        json_path = os.path.join(prompts_dir, f)
        entries = load_json(json_path)
        if entries is None:
            warnings.append(f"JSON解析失败: {f}")
            log_debug(f"JSON解析失败: {f}")
            txt_path = txt_files.get(base)
            if txt_path:
                content = read_file(txt_path)
                auto_entry = {
                    "id": len(prompts) + 1,
                    "tag": "未分类",
                    "file": base + ".txt",
                    "content": content or "",
                    "default_questions": [],
                }
                prompts.append(auto_entry)
                warnings.append(f"JSON损坏，已从TXT自动生成: {base}.txt")
            continue
        if not isinstance(entries, list):
            entries = [entries]
        txt_path = txt_files.get(base)
        content = read_file(txt_path) if txt_path else None
        if content is None:
            warnings.append(f"读取TXT失败或缺失: {base}.txt")
        for entry in entries:
            entry["file"] = f
            entry["content"] = content or ""
        prompts.extend(entries)
    for base, txt_path in txt_files.items():
        json_path = os.path.join(prompts_dir, base + ".json")
        if not os.path.exists(json_path):
            content = read_file(txt_path)
            auto_entry = {
                "id": len(prompts) + 1,
                "tag": "未分类",
                "file": base + ".txt",
                "content": content or "",
                "default_questions": [],
            }
            prompts.append(auto_entry)
            warnings.append(f"自动生成元数据: {base}.txt")
    return jsonify({"prompts": prompts, "warnings": warnings})


@app.route("/api/v1/test-set/questions", methods=["GET"])
def get_test_set_questions():
    test_set = request.args.get("test_set", "")
    if not test_set:
        return jsonify({"error": "Missing test_set parameter"}), 400
    if not validate_test_set_name(test_set):
        return jsonify({"error": "Invalid test_set name"}), 400
    questions_dir = resolve_test_set_path(test_set, "测试问题")
    if not os.path.exists(questions_dir):
        return jsonify({"questions": [], "warnings": ["目录不存在: 测试问题/"]})
    questions = []
    warnings = []
    for f in sorted(os.listdir(questions_dir)):
        if not f.endswith(".json"):
            continue
        if not validate_file_name(f):
            warnings.append(f"文件名不合法，已跳过: {f}")
            continue
        filepath = os.path.join(questions_dir, f)
        entries = load_json(filepath)
        if entries is None:
            warnings.append(f"JSON解析失败: {f}")
            log_debug(f"JSON解析失败: {f}")
            continue
        if not isinstance(entries, list):
            entries = [entries]
        for entry in entries:
            entry["file"] = f
            questions.append(entry)
    return jsonify({"questions": questions, "warnings": warnings})


_tags_cache = None
_tags_cache_by_set = None

def invalidate_tags_cache():
    global _tags_cache, _tags_cache_by_set
    _tags_cache = None
    _tags_cache_by_set = None

@app.route("/api/v1/tags", methods=["GET"])
def get_all_tags():
    global _tags_cache, _tags_cache_by_set
    if _tags_cache is not None and _tags_cache_by_set is not None:
        return jsonify({"tags": _tags_cache, "tags_by_set": _tags_cache_by_set})
    root = get_test_set_dir()
    all_tags = set()
    tags_by_set = {}
    if not os.path.exists(root):
        return jsonify({"tags": [], "tags_by_set": {}})
    for dir_name in os.listdir(root):
        dir_path = os.path.join(root, dir_name)
        if not os.path.isdir(dir_path) or dir_name.startswith("."):
            continue
        test_set_tags = set()
        prompts_dir = os.path.join(dir_path, "测试系统提示词")
        questions_dir = os.path.join(dir_path, "测试问题")
        for d in [prompts_dir, questions_dir]:
            if os.path.exists(d):
                for f in os.listdir(d):
                    if not f.endswith(".json"):
                        continue
                    file_entries = load_json(os.path.join(d, f))
                    if not isinstance(file_entries, list):
                        file_entries = [file_entries] if file_entries else []
                    for item in file_entries:
                        tag = item.get("tag", "")
                        if tag:
                            all_tags.add(tag)
                            test_set_tags.add(tag)
        tags_by_set[dir_name] = sorted(test_set_tags)
    _tags_cache = sorted(all_tags)
    _tags_cache_by_set = tags_by_set
    return jsonify({
        "tags": _tags_cache,
        "tags_by_set": tags_by_set,
    })


@app.route("/api/v1/test-set/results", methods=["GET"])
def get_test_set_results():
    test_set = request.args.get("test_set", "")
    if not test_set:
        return jsonify({"error": "Missing test_set parameter"}), 400
    if not validate_test_set_name(test_set):
        return jsonify({"error": "Invalid test_set name"}), 400
    results_dir = resolve_test_set_path(test_set, "测试结果")
    if not os.path.exists(results_dir):
        return jsonify({"results": []})
    files = []
    for f in sorted(os.listdir(results_dir), reverse=True):
        if f.endswith(".json") and not f.startswith("_"):
            filepath = os.path.join(results_dir, f)
            data = load_json(filepath)
            files.append({
                "name": f.replace(".json", ""),
                "data": data or [],
            })
    return jsonify({"results": files})


@app.route("/api/v1/canvas-state", methods=["GET", "POST"])
def handle_canvas_state():
    canvas_file = os.path.join(DATA_DIR, "canvas_state.json")
    if request.method == "GET":
        data = load_json(canvas_file)
        if data:
            return jsonify(data)
        return jsonify({"nodes": [], "connections": []})
    data = request.get_json() or {}
    if request.content_length and request.content_length > 1024 * 1024:
        return jsonify({"error": "请求体超过大小限制（1MB）"}), 413
    if not isinstance(data, dict):
        return jsonify({"error": "请求体必须为JSON对象"}), 400
    save_json(canvas_file, data)
    return jsonify({"status": "ok"})


@app.route("/api/v1/stop-tests", methods=["POST"])
def stop_tests():
    global stop_generation
    with stop_lock:
        stop_generation += 1
    return jsonify({"status": "ok"})


# ============ AI Call ============

def _build_payload(model_name, system_prompt, user_prompt, temperature, top_p, top_k=None, min_p=None, context_size=None):
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "top_p": top_p,
    }
    if top_k is not None:
        payload["top_k"] = top_k
    if min_p:
        payload["min_p"] = min_p
    if context_size is not None and context_size > 0:
        payload["context_size"] = context_size
    return payload


def _parse_sse_lines(lines_iter):
    content = ""
    for raw_line in lines_iter:
        if raw_line:
            try:
                decoded = raw_line.decode("utf-8")
            except UnicodeDecodeError:
                continue
            if not decoded.startswith("data: "):
                continue
            data_str = decoded[6:].strip()
            if data_str == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
                delta = chunk.get("choices", [{}])[0].get("delta", {})
                content_delta = delta.get("content", "")
                if content_delta:
                    content += content_delta
            except json.JSONDecodeError:
                continue
    return content


def _parse_sse_stream(response):
    return _parse_sse_lines(response.iter_lines())


def _parse_sse_from_body(raw_body):
    return _parse_sse_lines(raw_body.split(b'\n'))


def _handle_streaming_response(response, attempt):
    content_type = response.headers.get("Content-Type", "")
    content = None
    if "text/event-stream" in content_type:
        content = _parse_sse_stream(response)
    if content:
        return {"success": True, "content": content}
    raw_body = response.content
    try:
        result = json.loads(raw_body)
        if result.get("choices") and result["choices"][0].get("message"):
            content = result["choices"][0]["message"].get("content")
            if content:
                return {"success": True, "content": content}
        log_debug(f"AI流式模式返回JSON，attempt={attempt}, response={result}")
    except Exception:
        pass
    content = _parse_sse_from_body(raw_body)
    if content:
        return {"success": True, "content": content}
    log_debug(f"AI流式返回为空，attempt={attempt}")
    return None


def _handle_non_streaming_response(response, attempt):
    try:
        result = response.json()
    except (json.JSONDecodeError, ValueError) as e:
        log_debug(f"非流式响应JSON解析失败，attempt={attempt}: {e}")
        return None
    if result.get("choices") and result["choices"][0].get("message"):
        content = result["choices"][0]["message"].get("content")
        if content:
            return {"success": True, "content": content}
    log_debug(f"AI返回为空，attempt={attempt}, response={result}")
    return None


def call_ai(system_prompt, user_prompt, model=None, max_retries=None, timeout=None, run_gen=None):
    with config_lock:
        if max_retries is None:
            max_retries = config.get("max_retries", 3)
        if timeout is None:
            timeout = config.get("timeout", 60)
        api_key = config.get("api_key", "")
        base_url = config.get("base_url", "http://localhost:8000/v1")
        temperature = config.get("temperature", 0.7)
        top_p = config.get("top_p", 1.0)
        model_name = model or config.get("model", "gpt-4o")
        top_k = config.get("top_k")
        min_p = config.get("min_p")
        context_size = config.get("context_size")
        streaming = config.get("streaming", False)

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = _build_payload(model_name, system_prompt, user_prompt, temperature, top_p, top_k, min_p, context_size)

    for attempt in range(max_retries):
        if should_stop(run_gen):
            return None
        try:
            req_payload = dict(payload)
            if streaming:
                req_payload["stream"] = True
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=req_payload,
                stream=streaming,
                timeout=timeout,
            )
            if response.status_code == 200:
                if streaming:
                    result = _handle_streaming_response(response, attempt)
                else:
                    result = _handle_non_streaming_response(response, attempt)
                if result:
                    return result
            elif response.status_code == 429:
                if should_stop(run_gen): return {"success": False, "error_type": "cancelled", "error_msg": "已取消"}
                time.sleep(2**attempt)
            elif 400 <= response.status_code < 500:
                log_debug(f"AI请求客户端错误，status={response.status_code}，不重试")
                return {"success": False, "error_type": "client_error", "error_msg": f"HTTP {response.status_code}: {response.text[:200]}"}
            else:
                log_debug(
                    f"AI请求失败，status={response.status_code}, response={response.text}"
                )
                if should_stop(run_gen): return {"success": False, "error_type": "cancelled", "error_msg": "已取消"}
                time.sleep(2**attempt)
        except requests.exceptions.Timeout:
            log_debug(f"AI请求超时，attempt={attempt}")
            if should_stop(run_gen): return {"success": False, "error_type": "cancelled", "error_msg": "已取消"}
            time.sleep(2**attempt)
        except Exception as e:
            log_debug(f"AI请求异常: {e}")
            if should_stop(run_gen): return {"success": False, "error_type": "cancelled", "error_msg": "已取消"}
            time.sleep(2**attempt)
    return {"success": False, "error_type": "api_error", "error_msg": "API请求失败"}


# ============ NEW: Run Tests (Cartesian Product) ============

@app.route("/api/v1/run-tests", methods=["POST"])
def run_tests():
    global stop_generation
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    with stop_lock:
        current_gen = stop_generation

    with config_lock:
        concurrency = config.get("concurrency", 1)
        test_count = config.get("test_count", 1)

    test_set = data.get("test_set")
    prompts_data = data.get("prompts", [])
    questions_data = data.get("questions", [])
    models = data.get("models", [])
    if not models:
        with config_lock:
            models = [config.get("model", "gpt-4o")]

    if not test_set or not prompts_data or not questions_data:
        return jsonify({"error": "No test items specified"}), 400

    if not validate_test_set_name(test_set):
        return jsonify({"error": "Invalid test_set name"}), 400

    return run_tests_cartesian(test_set, prompts_data, questions_data, models, concurrency, test_count, current_gen)


def should_stop(run_gen):
    with stop_lock:
        return stop_generation != run_gen

def run_tests_cartesian(test_set, prompts, questions, models, concurrency, test_count, current_gen):
    MAX_TASKS = 10000
    total_tasks = len(prompts) * len(questions) * len(models)
    if total_tasks == 0:
        return jsonify({"error": "No test items (cartesian product is empty)"}), 400
    if total_tasks > MAX_TASKS:
        return jsonify({"error": f"任务数 {total_tasks} 超过上限 {MAX_TASKS}，请减少测试项数量"}), 400

    task_queue = []
    for p in prompts:
        for q in questions:
            for m in models:
                task_queue.append((p, q, m))

    def generate():
        completed = 0
        failed = 0
        all_results = []
        results_lock = threading.Lock()
        disconnected = threading.Event()

        try:
            yield f"data: {json.dumps({'type': 'status', 'message': f'共 {total_tasks} 个测试任务, 并发数 {concurrency}, 正在生成...'}, ensure_ascii=False)}\n\n"

            def run_task(task):
                p, q, m = task
                if should_stop(current_gen):
                    return None

                system_prompt = p.get("content", "")
                if system_prompt:
                    prompt_type = p.get("type", "content")
                    if prompt_type == "instruction":
                        pass
                    else:
                        wrapper = "以下是被测试的文件内容：\n\n{content}\n\n请根据以上文件内容回答用户的问题。"
                        system_prompt = wrapper.replace("{content}", system_prompt)

                user_prompt = q.get("question", "")
                expected_answer = q.get("answer", "")

                multi_answers = []
                for i in range(test_count):
                    if should_stop(current_gen):
                        break
                    reply = call_ai(system_prompt, user_prompt, model=m, run_gen=current_gen)
                    if reply is None:
                        return None
                    if isinstance(reply, dict) and reply.get("success"):
                        multi_answers.append({"index": i + 1, "answer": reply["content"]})
                    elif isinstance(reply, dict) and not reply.get("success"):
                        return {
                            "id": f"p{p.get('id', '?')}_q{q.get('id', '?')}_m{m}",
                            "prompt_id": p.get("id"),
                            "question_id": q.get("id"),
                            "model_id": m,
                            "prompt_tag": p.get("tag", ""),
                            "question_tag": q.get("tag", ""),
                            "question": user_prompt,
                            "answer": expected_answer,
                            "model_reply": None,
                            "multi_answers": multi_answers,
                            "error_type": reply.get("error_type"),
                            "error_msg": reply.get("error_msg"),
                        }

                first_reply = multi_answers[0]["answer"] if multi_answers else None

                result = {
                    "id": f"p{p.get('id', '?')}_q{q.get('id', '?')}_m{m}",
                    "prompt_id": p.get("id"),
                    "question_id": q.get("id"),
                    "model_id": m,
                    "prompt_tag": p.get("tag", ""),
                    "question_tag": q.get("tag", ""),
                    "question": user_prompt,
                    "answer": expected_answer,
                    "model_reply": first_reply,
                    "multi_answers": multi_answers,
                }
                return result

            with ThreadPoolExecutor(max_workers=min(max(1, concurrency), 20)) as executor:
                futures = {executor.submit(run_task, task): task for task in task_queue}
                for future in as_completed(futures):
                    if should_stop(current_gen) or disconnected.is_set():
                        if sys.version_info >= (3, 9):
                            executor.shutdown(wait=False, cancel_futures=True)
                        else:
                            executor.shutdown(wait=False)
                        reason = '测试已终止' if should_stop(current_gen) else '客户端已断开'
                        yield f"data: {json.dumps({'type': 'status', 'message': reason}, ensure_ascii=False)}\n\n"
                        if all_results:
                            try:
                                for r in all_results:
                                    r["is_cancelled"] = True
                                save_results_to_test_set(test_set, all_results)
                                yield f"data: {json.dumps({'type': 'done', 'message': '测试已中断，部分结果已保存', 'total_results': len(all_results)}, ensure_ascii=False)}\n\n"
                            except (OSError, IOError) as e:
                                log_debug(f"中断保存结果失败: {e}")
                                yield f"data: {json.dumps({'type': 'status', 'message': f'中断保存结果失败: {e}'}, ensure_ascii=False)}\n\n"
                                yield f"data: {json.dumps({'type': 'done', 'message': '中断保存失败', 'total_results': len(all_results)}, ensure_ascii=False)}\n\n"
                        else:
                            yield f"data: {json.dumps({'type': 'done', 'message': '测试已中断，无结果', 'total_results': 0}, ensure_ascii=False)}\n\n"
                        return
                    try:
                        result = future.result()
                    except Exception as e:
                        log_debug(f"Task failed: {e}")
                        completed += 1
                        failed += 1
                        error_result = {
                            "type": "error",
                            "error_type": type(e).__name__,
                            "error_msg": str(e),
                            "completed": completed,
                            "total": total_tasks,
                        }
                        yield f"data: {json.dumps(error_result, ensure_ascii=False)}\n\n"
                        continue
                    if result is None:
                        continue

                    with results_lock:
                        all_results.append(result)
                    completed += 1

                    if completed % INCREMENTAL_SAVE_STEP == 0:
                        try:
                            save_results_to_test_set(test_set, all_results, incremental=True)
                        except (OSError, IOError) as e:
                            log_debug(f"Incremental save failed: {e}")

                    sse_data = {
                        'type': 'result',
                        'id': result['id'],
                        'prompt_id': result['prompt_id'],
                        'question_id': result['question_id'],
                        'model_id': result['model_id'],
                        'prompt_tag': result['prompt_tag'],
                        'question': result['question'],
                        'expected_answer': result['answer'],
                        'ai_answer': result['model_reply'] or '',
                        'multi_answers': result.get('multi_answers', []),
                        'test_count': len(result.get('multi_answers', [])),
                        'requested_test_count': test_count,
                        'completed': completed,
                        'total': total_tasks,
                    }
                    if 'error_type' in result:
                        sse_data['error_type'] = result['error_type']
                        sse_data['error_msg'] = result['error_msg']
                    yield f"data: {json.dumps(sse_data, ensure_ascii=False)}\n\n"
        finally:
            disconnected.set()

        # Save results
        try:
            save_results_to_test_set(test_set, all_results)
            incr_path = resolve_test_set_path(test_set, "测试结果", INCREMENTAL_FILE)
            if os.path.exists(incr_path):
                os.remove(incr_path)
        except (OSError, IOError) as e:
            log_debug(f"保存结果失败: {e}")
            yield f"data: {json.dumps({'type': 'status', 'message': f'保存结果失败: {e}'}, ensure_ascii=False)}\n\n"

        yield f"data: {json.dumps({'type': 'done', 'message': '测试完成', 'total_results': len(all_results)}, ensure_ascii=False)}\n\n"

    return Response(generate(), mimetype="text/event-stream")


INCREMENTAL_SAVE_STEP = 10  # 可从config读取（若需要）
INCREMENTAL_FILE = "_incremental.json"

def save_results_to_test_set(test_set, results, incremental=False):
    results_dir = resolve_test_set_path(test_set, "测试结果")
    os.makedirs(results_dir, exist_ok=True)
    if incremental:
        filepath = os.path.join(results_dir, INCREMENTAL_FILE)
    else:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        suffix = uuid.uuid4().hex[:8]
        filepath = os.path.join(results_dir, f"{ts}_{suffix}.json")
    save_json(filepath, results)
    if not incremental:
        try:
            all_files = sorted([f for f in os.listdir(results_dir) if f.endswith(".json") and not f.startswith("_")])
            while len(all_files) > 20:
                old = all_files.pop(0)
                try:
                    os.remove(os.path.join(results_dir, old))
                except FileNotFoundError:
                    pass
        except OSError:
            pass


ARCHIVES_DIR = os.path.join(BASE_DIR, "linksave")
ARCHIVES_FILE = os.path.join(ARCHIVES_DIR, "archives.json")

@app.route("/api/v1/archives", methods=["GET", "POST", "DELETE"])
def handle_archives():
    os.makedirs(ARCHIVES_DIR, exist_ok=True)
    if request.method == "GET":
        data = load_json(ARCHIVES_FILE)
        return jsonify(data or [])
    if request.method == "POST":
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "数据格式无效"}), 400
        save_json(ARCHIVES_FILE, data)
        return jsonify({"status": "ok"})
    if request.method == "DELETE":
        body = request.get_json() or {}
        archive_id = body.get("id")
        if not archive_id:
            return jsonify({"error": "缺少存档ID"}), 400
        archives = load_json(ARCHIVES_FILE) or []
        archives = [a for a in archives if a.get("id") != archive_id]
        save_json(ARCHIVES_FILE, archives)
        return jsonify({"status": "ok"})


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    log_debug(f"Internal server error: {e}")
    return jsonify({"error": "服务器内部错误"}), 500


if __name__ == "__main__":
    for dir_path in [DATA_DIR, ARCHIVES_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    load_config()
    app.run(debug=os.environ.get('FLASK_DEBUG', '0') == '1', port=5000, threaded=True)
