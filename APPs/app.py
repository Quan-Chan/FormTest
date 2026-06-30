import os
import json
import requests
import threading
import queue
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
active_jobs = {}
active_jobs_lock = threading.Lock()

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
    "known_test_sets": [],
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


def is_json_file(filename):
    """Check if a filename has a .json extension (case-insensitive)."""
    return isinstance(filename, str) and filename.lower().endswith(".json")


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


def validate_test_set_name_strict(name):
    """Validate test set name without checking against get_test_set_dir().
    Suitable for custom-path creation."""
    if not name:
        return False
    if ".." in name or "/" in name or "\\" in name:
        return False
    if name != os.path.basename(name):
        return False
    if sys.platform == "win32":
        reserved = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
                     "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3",
                     "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}
        if os.path.splitext(name)[0].upper() in reserved:
            return False
    return True


def _record_known_test_set(name, path):
    """Record a test set in the known_test_sets config list."""
    with config_lock:
        known = config.get("known_test_sets", [])
        for entry in known:
            if entry.get("name") == name and entry.get("path") == path:
                entry["last_used"] = int(time.time() * 1000)
                break
        else:
            known.append({"name": name, "path": path, "last_used": int(time.time() * 1000)})
        config["known_test_sets"] = known
        save_config()

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
    for f in sorted(os.listdir(prompts_dir)):
        if not is_json_file(f):
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
            continue
        if not isinstance(entries, list):
            entries = [entries]
        for entry in entries:
            entry["file"] = f
            if "content" not in entry or not entry["content"]:
                entry["content"] = ""
                warnings.append(f"条目缺失content，已置空: {base}.json")
        prompts.extend(entries)
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
        if not is_json_file(f):
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
                    if not is_json_file(f):
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


@app.route("/api/v1/test-set/create", methods=["POST"])
def create_test_set():
    data = request.get_json()
    base_path = data.get("base_path", "")
    name = data.get("name", "")
    question_groups = data.get("question_groups", [])
    prompt_groups = data.get("prompt_groups", [])

    if not name:
        return jsonify({"error": "测试集名称不能为空"}), 400
    if not validate_test_set_name_strict(name):
        return jsonify({"error": "测试集名称不合法"}), 400
    if not base_path:
        return jsonify({"error": "保存路径不能为空"}), 400

    abs_path = os.path.abspath(base_path)
    if not os.path.isdir(abs_path):
        return jsonify({"error": f"保存路径不存在: {abs_path}"}), 400

    qa_count = sum(len(g.get("items", [])) for g in question_groups)
    prompt_count = sum(len(g.get("items", [])) for g in prompt_groups)
    if qa_count < 1 or prompt_count < 1:
        return jsonify({"error": "至少需要 1 个问答对和 1 个提示词"}), 400

    # ── Phase 1: Validate all input before creating any files ──
    for group in question_groups:
        filename = group.get("filename", "").strip()
        if not filename:
            return jsonify({"error": "问题组的文件名不能为空"}), 400
        tag = group.get("tag", "")
        for i, item in enumerate(group.get("items", [])):
            if not item.get("question", "").strip() or not item.get("answer", "").strip():
                return jsonify({"error": f"问题组「{tag}」第 {i+1} 项存在空内容"}), 400

    for group in prompt_groups:
        filename = group.get("filename", "").strip()
        if not filename:
            return jsonify({"error": "提示词组的文件名不能为空"}), 400
        tag = group.get("tag", "")
        for i, item in enumerate(group.get("items", [])):
            if not item.get("content", "").strip():
                return jsonify({"error": f"提示词组「{tag}」第 {i+1} 项存在空内容"}), 400

    # ── Phase 2: Create directory structure ──
    test_set_path = os.path.join(abs_path, name)
    # Use os.mkdir to atomically create the root dir (fails if exists) — avoids TOCTOU race
    try:
        os.mkdir(test_set_path)
    except FileExistsError:
        return jsonify({"error": f"该位置已存在同名测试集「{name}」，请修改名称后重试"}), 409
    except OSError as e:
        return jsonify({"error": f"创建目录失败: {str(e)}"}), 500

    created_dirs = []
    try:
        for subdir in ["测试系统提示词", "测试问题", "测试结果"]:
            os.makedirs(os.path.join(test_set_path, subdir), exist_ok=True)
            created_dirs.append(os.path.join(test_set_path, subdir))
    except OSError as e:
        _cleanup_created(test_set_path, created_dirs)
        return jsonify({"error": f"创建目录失败: {str(e)}"}), 500

    # ── Phase 3: Write files (validation already done in Phase 1) ──
    written_files = []
    try:
        for group in question_groups:
            filename = group.get("filename", "").strip()
            if not is_json_file(filename):
                filename += ".json"
            tag = group.get("tag", "")
            items = group.get("items", [])
            entries = [
                {"id": i + 1, "tag": tag, "question": item.get("question", ""), "answer": item.get("answer", "")}
                for i, item in enumerate(items)
            ]
            save_json(os.path.join(test_set_path, "测试问题", filename), entries)
            written_files.append(os.path.join(test_set_path, "测试问题", filename))

        for group in prompt_groups:
            filename = group.get("filename", "").strip()
            if not is_json_file(filename):
                filename += ".json"
            tag = group.get("tag", "")
            default_qs = []
            for f in group.get("default_questions", []):
                fn = f if is_json_file(f) else f + ".json"
                default_qs.append(f"测试问题/{fn}")
            items = group.get("items", [])
            entries = [
                {"id": i + 1, "tag": tag, "default_questions": default_qs, "content": item.get("content", "")}
                for i, item in enumerate(items)
            ]
            save_json(os.path.join(test_set_path, "测试系统提示词", filename), entries)
            written_files.append(os.path.join(test_set_path, "测试系统提示词", filename))
    except OSError as e:
        _cleanup_created(test_set_path, created_dirs, written_files)
        return jsonify({"error": f"创建测试集失败: {str(e)}"}), 500

    invalidate_tags_cache()
    try:
        _record_known_test_set(name, test_set_path)
    except Exception as e:
        log_debug(f"[create_test_set] 记录已知测试集失败: {e}")
    return jsonify({"success": True, "path": test_set_path})


def _cleanup_created(root_path, dirs=None, files=None):
    """Rollback: remove created files and directories on failure."""
    if files:
        for f in files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except OSError:
                pass
    if dirs:
        for d in reversed(dirs):
            try:
                if os.path.isdir(d):
                    os.rmdir(d)
            except OSError:
                pass
    try:
        if os.path.isdir(root_path):
            os.rmdir(root_path)
    except OSError:
        pass


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
        if is_json_file(f) and not f.startswith("_"):
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
    raw = request.get_data()
    if len(raw) > 1024 * 1024:
        return jsonify({"error": "请求体超过大小限制（1MB）"}), 413
    try:
        data = json.loads(raw) if raw else {}
    except (json.JSONDecodeError, ValueError):
        data = {}
    if not isinstance(data, dict):
        return jsonify({"error": "请求体必须为JSON对象"}), 400
    save_json(canvas_file, data)
    return jsonify({"status": "ok"})


@app.route("/api/v1/test-job/stop/<job_id>", methods=["POST"])
def stop_test_job(job_id):
    with active_jobs_lock:
        job = active_jobs.get(job_id)
    if job is None:
        return jsonify({"error": "Job not found"}), 404
    job.stop()
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
    if min_p is not None:
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


def call_ai_atomic(system_prompt, user_prompt, model=None, timeout=None):
    """Single AI call - no retry. Returns {success, content?} or {rate_limited: True}."""
    with config_lock:
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
                result = _handle_streaming_response(response, 0)
            else:
                result = _handle_non_streaming_response(response, 0)
            if result:
                return result
            return {"success": False, "error": "Empty AI response"}
        elif response.status_code == 429:
            return {"rate_limited": True}
        elif 400 <= response.status_code < 500:
            log_debug(f"AI请求客户端错误，status={response.status_code}，不重试")
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text[:200]}"}
        else:
            log_debug(f"AI请求失败，status={response.status_code}，将重试")
            return {"retry": True}
    except requests.exceptions.Timeout:
        log_debug(f"AI请求超时，将重试")
        return {"retry": True}
    except Exception as e:
        log_debug(f"AI请求异常: {e}")
        return {"success": False, "error": str(e)}


# ============ Test Job System ============

def _run_single_task(task):
    """Wrap system prompt and call AI. Returns raw result dict from call_ai_atomic."""
    system_prompt = task.prompt.get("content", "")
    if system_prompt:
        prompt_type = task.prompt.get("type", "content")
        if prompt_type != "instruction":
            wrapper = "以下是被测试的文件内容：\n\n{content}\n\n请根据以上文件内容回答用户的问题。"
            system_prompt = wrapper.replace("{content}", system_prompt)
    user_prompt = task.question.get("question", "")
    return call_ai_atomic(system_prompt, user_prompt, model=task.model)


class TestTask:
    __slots__ = ('seq', 'test_set_name', 'prompt', 'question', 'model', 'test_index',
                 'status', 'retry_count', 'backoff_until', 'result')

    def __init__(self, seq, test_set_name, prompt, question, model, test_index):
        self.seq = seq
        self.test_set_name = test_set_name
        self.prompt = prompt
        self.question = question
        self.model = model
        self.test_index = test_index
        self.status = "pending"
        self.retry_count = 0
        self.backoff_until = 0
        self.result = None


class TestJob:
    def __init__(self, job_id, test_sets, models, concurrency, test_count):
        self.job_id = job_id
        self.tasks = []
        self.pending = []
        self.rate_limited = []
        self.results = {}
        self.results_by_set = {}
        self.concurrency = concurrency
        self.test_count = test_count
        self.status = "running"
        self.stop_event = threading.Event()
        self.subscribers = []
        self.total = 0
        self.completed = 0
        self.failed = 0
        self.executor = None
        self.futures = {}
        self.lock = threading.Lock()
        self.write_lock = threading.Lock()

        seq = 0
        for ts in test_sets:
            name = ts["name"]
            prompts = ts.get("prompts", [])
            questions = ts.get("questions", [])
            for p in prompts:
                for q in questions:
                    for m in models:
                        for i in range(test_count):
                            seq += 1
                            task = TestTask(seq, name, p, q, m, i)
                            self.tasks.append(task)
        self.total = len(self.tasks)
        self.pending = list(self.tasks)

    def _get_backoff(self, retry_count):
        if retry_count < 6:
            return 2 ** (retry_count + 1)
        return 60

    def add_subscriber(self, q):
        with self.lock:
            for seq in sorted(self.results.keys()):
                q.put(("result", self.results[seq]))
            q.put(("progress", {"completed": self.completed, "total": self.total, "failed": self.failed}))
            self.subscribers.append(q)

    def remove_subscriber(self, q):
        with self.lock:
            self.subscribers = [s for s in self.subscribers if s is not q]

    def _broadcast(self, event_type, data):
        with self.lock:
            dead = []
            for s in self.subscribers:
                try:
                    s.put_nowait((event_type, data))
                except queue.Full:
                    dead.append(s)
            for d in dead:
                self.subscribers.remove(d)

    def _find_task(self, seq):
        for task in self.tasks:
            if task.seq == seq:
                return task
        return None

    def _build_result_item(self, task, result):
        item = {
            "test_set": task.test_set_name,
            "id": f"p{task.prompt.get('id', '?')}_q{task.question.get('id', '?')}_m{task.model}_{task.test_index}",
            "prompt_id": task.prompt.get("id"),
            "question_id": task.question.get("id"),
            "model_id": task.model,
            "prompt_tag": task.prompt.get("tag", ""),
            "question_tag": task.question.get("tag", ""),
            "question": task.question.get("question", ""),
            "expected_answer": task.question.get("answer", ""),
            "test_index": task.test_index + 1,
            "test_count": self.test_count,
        }
        if result.get("success"):
            item["ai_answer"] = result["content"]
        else:
            item["ai_answer"] = None
            item["error_type"] = result.get("error", "")
            item["error_msg"] = result.get("error", "")
        return item

    def run_scheduler(self):
        try:
            with self.lock:
                self.executor = ThreadPoolExecutor(max_workers=self.concurrency)

            while self.status == "running":
                self._collect_futures()
                self._check_rate_limited()
                self._dispatch_tasks()

                if self._is_done():
                    self.status = "completed"
                    self._broadcast("status", {"status": "completed", "message": "测试完成"})
                    break

                if self.stop_event.is_set():
                    self.status = "stopped"
                    self._broadcast("status", {"status": "stopped", "message": "测试已终止"})
                    break

                time.sleep(0.05)
        except Exception as e:
            log_debug(f"Scheduler error for job {self.job_id}: {e}")
            self.status = "error"
            self._broadcast("status", {"status": "error", "message": str(e)})
        finally:
            self._finalize()

    def _collect_futures(self):
        with self.lock:
            done_seqs = [seq for seq, f in self.futures.items() if f.done()]

        for seq in done_seqs:
            with self.lock:
                future = self.futures.pop(seq, None)
            if future is None:
                continue
            try:
                result = future.result(timeout=0)
            except Exception as e:
                result = {"success": False, "error": str(e)}

            task = self._find_task(seq)
            if task is None:
                continue

            if result.get("rate_limited") or result.get("retry"):
                task.retry_count += 1
                if task.retry_count > 12:
                    task.status = "error"
                    task.result = {"success": False, "error": "Exceeded retry limit after 12 retries"}
                    self.completed += 1
                    self.failed += 1
                else:
                    backoff = self._get_backoff(task.retry_count)
                    task.backoff_until = time.time() + backoff
                    task.status = "rate_limited"
                    self.rate_limited.append(task)
                    log_debug(f"Task {seq} rate limited, retry {task.retry_count}, backoff {backoff}s")
                    continue
            elif result.get("success"):
                task.status = "done"
                task.result = result
                self.completed += 1
            else:
                task.status = "error"
                task.result = result
                self.completed += 1
                self.failed += 1

            item = self._build_result_item(task, result)
            with self.lock:
                self.results[seq] = item
                ts_name = task.test_set_name
                if ts_name not in self.results_by_set:
                    self.results_by_set[ts_name] = []
                self.results_by_set[ts_name].append(item)

            self._broadcast("result", item)
            self._broadcast("progress", {"completed": self.completed, "total": self.total, "failed": self.failed})

            if self.completed % INCREMENTAL_SAVE_STEP == 0:
                self._incremental_save()

    def _check_rate_limited(self):
        now = time.time()
        ready = []
        with self.lock:
            for task in self.rate_limited:
                if task.backoff_until <= now:
                    ready.append(task)
            for task in ready:
                self.rate_limited.remove(task)
                task.status = "pending"
                self.pending.insert(0, task)

    def _dispatch_tasks(self):
        with self.lock:
            available = self.concurrency - len(self.futures)
            for _ in range(available):
                if not self.pending:
                    break
                task = self.pending.pop(0)
                task.status = "running"
                future = self.executor.submit(_run_single_task, task)
                self.futures[task.seq] = future

    def _is_done(self):
        with self.lock:
            return (not self.pending and not self.rate_limited and not self.futures)

    def _incremental_save(self):
        with self.write_lock:
            for ts_name, results in self.results_by_set.items():
                save_results_to_test_set(ts_name, list(results), incremental=True)

    def _finalize(self):
        with self.write_lock:
            for ts_name, results in self.results_by_set.items():
                save_results_to_test_set(ts_name, list(results))
                incr_path = resolve_test_set_path(ts_name, "测试结果", INCREMENTAL_FILE)
                if os.path.exists(incr_path):
                    try:
                        os.remove(incr_path)
                    except OSError:
                        pass

        self._broadcast("done", {"status": self.status, "message": "测试完成" if self.status == "completed" else "测试已终止"})

        if self.executor:
            try:
                self.executor.shutdown(wait=False)
            except Exception:
                pass

        with active_jobs_lock:
            active_jobs.pop(self.job_id, None)

    def stop(self):
        self.stop_event.set()


@app.route("/api/v1/test-job/submit", methods=["POST"])
def submit_test_job():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    with config_lock:
        concurrency = config.get("concurrency", 1)
        test_count = config.get("test_count", 1)

    test_sets = data.get("test_sets", [])
    models = data.get("models", [])

    if not models:
        with config_lock:
            models = [config.get("model", "gpt-4o")]

    if not test_sets:
        return jsonify({"error": "No test sets specified"}), 400

    for ts in test_sets:
        if not validate_test_set_name(ts.get("name", "")):
            return jsonify({"error": f"Invalid test_set name: {ts.get('name')}"}), 400

    job_id = uuid.uuid4().hex
    job = TestJob(job_id, test_sets, models, concurrency, test_count)

    if job.total == 0:
        return jsonify({"error": "No test items (cartesian product is empty)"}), 400

    MAX_TASKS = 10000
    if job.total > MAX_TASKS:
        return jsonify({"error": f"任务数 {job.total} 超过上限 {MAX_TASKS}，请减少测试项数量"}), 400

    with active_jobs_lock:
        active_jobs[job_id] = job

    thread = threading.Thread(target=job.run_scheduler, name=f"Job-{job_id[:8]}")
    thread.daemon = True
    thread.start()

    return jsonify({"job_id": job_id, "total_tasks": job.total})


@app.route("/api/v1/test-job/stream/<job_id>", methods=["GET"])
def stream_test_job(job_id):
    with active_jobs_lock:
        job = active_jobs.get(job_id)
    if job is None:
        return jsonify({"error": "Job not found"}), 404

    sub_queue = queue.Queue()

    def generate():
        job.add_subscriber(sub_queue)
        try:
            while True:
                try:
                    event_type, data = sub_queue.get(timeout=30)
                except queue.Empty:
                    yield f"data: {json.dumps({'type': 'heartbeat'}, ensure_ascii=False)}\n\n"
                    if job.status != "running":
                        break
                    continue

                if event_type == "result":
                    payload = {
                        'type': 'result',
                        'test_set': data['test_set'],
                        'id': data['id'],
                        'prompt_id': data['prompt_id'],
                        'question_id': data['question_id'],
                        'model_id': data['model_id'],
                        'prompt_tag': data['prompt_tag'],
                        'question_tag': data['question_tag'],
                        'question': data['question'],
                        'expected_answer': data['expected_answer'],
                        'ai_answer': data['ai_answer'] or '',
                        'test_index': data['test_index'],
                        'test_count': data['test_count'],
                    }
                    if data.get('error_type'):
                        payload['error_type'] = data['error_type']
                        payload['error_msg'] = data['error_msg']
                    yield "data: " + json.dumps(payload, ensure_ascii=False) + "\n\n"
                elif event_type == "progress":
                    yield f"data: {json.dumps({'type': 'progress', 'completed': data['completed'], 'total': data['total'], 'failed': data.get('failed', 0)}, ensure_ascii=False)}\n\n"
                elif event_type == "done":
                    yield f"data: {json.dumps({'type': 'done', 'status': data['status'], 'message': data['message']}, ensure_ascii=False)}\n\n"
                    break
                elif event_type == "status":
                    yield f"data: {json.dumps({'type': 'status', 'status': data['status'], 'message': data['message']}, ensure_ascii=False)}\n\n"
                    if data['status'] in ("completed", "stopped", "error"):
                        break
        except GeneratorExit:
            pass
        finally:
            job.remove_subscriber(sub_queue)

    return Response(generate(), mimetype="text/event-stream")


@app.route("/api/v1/test-job/status/<job_id>", methods=["GET"])
def get_test_job_status(job_id):
    with active_jobs_lock:
        job = active_jobs.get(job_id)
    if job is None:
        return jsonify({"status": "not_found"}), 404
    return jsonify({
        "status": job.status,
        "completed": job.completed,
        "total": job.total,
        "failed": job.failed,
    })


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
            all_files = sorted([f for f in os.listdir(results_dir) if is_json_file(f) and not f.startswith("_")])
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


# ============ Known Test Sets ============

@app.route("/api/v1/test-set/known/check", methods=["POST"])
def check_known_test_sets():
    data = request.get_json() or {}
    known = data.get("known_test_sets", [])
    if not known:
        with config_lock:
            known = config.get("known_test_sets", [])
    results = []
    for entry in known:
        path = entry.get("path", "")
        results.append({
            "name": entry.get("name", ""),
            "path": path,
            "available": bool(path and os.path.exists(path) and os.path.isdir(path)),
            "last_used": entry.get("last_used", 0)
        })
    return jsonify({"test_sets": results})


@app.route("/api/v1/test-set/known/set-dir", methods=["POST"])
def set_test_set_dir():
    data = request.get_json() or {}
    new_dir = data.get("test_set_dir", "")
    if not new_dir:
        return jsonify({"error": "路径不能为空"}), 400
    if not os.path.isdir(new_dir):
        return jsonify({"error": "路径不存在"}), 400
    with config_lock:
        config["test_set_dir"] = new_dir
        save_config()
    return scan_test_sets()


@app.route("/api/v1/test-set/known/record", methods=["POST"])
def record_known_test_sets():
    data = request.get_json() or {}
    sets = data.get("test_sets", [])
    if not isinstance(sets, list):
        return jsonify({"error": "数据格式无效"}), 400
    with config_lock:
        known = config.get("known_test_sets", [])
        for item in sets:
            name = item.get("name", "")
            path = item.get("path", "")
            if not name or not path:
                continue
            found = False
            for entry in known:
                if entry.get("name") == name and entry.get("path") == path:
                    entry["last_used"] = int(time.time() * 1000)
                    found = True
                    break
            if not found:
                known.append({"name": name, "path": path, "last_used": int(time.time() * 1000)})
        config["known_test_sets"] = known
        save_config()
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
