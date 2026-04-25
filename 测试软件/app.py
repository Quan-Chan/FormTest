import os
import json
import requests
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

app = Flask(__name__, static_folder="static")
CORS(app)


@app.route("/")
def index():
    return app.send_static_file("index.html")


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TESTS_DIR = os.path.join(os.path.dirname(__file__), "tests")
SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
ANSWER_CACHE_DIR = os.path.join(os.path.dirname(__file__), "Answer Cache")

config = {
    "api_key": "",
    "base_url": "http://192.168.1.45:1919/v1",
    "model": "qwen3.5-0.8b",
    "temperature": 0.7,
    "top_p": 1.0,
    "top_k": 40,
    "min_p": 0.05,
    "context_size": 8192,
    "concurrency": 1,
    "test_count": 1,
    "max_retries": 3,
    "streaming": True,
    "test_set_dir": "D:/文件/提示词/草稿A/测试集",
    "system_dir": "system",
    "questions_dir": "questions",
    "bindings_file": "bindings.json",
    "stop_flag": False,
}

bindings = {}


def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return None


def get_test_set_dir():
    if config.get("test_set_dir"):
        return config["test_set_dir"]
    return os.path.join(os.path.dirname(__file__), "..", "测试集")


def log_debug(msg):
    log_file = os.path.join(os.path.dirname(__file__), "debug.log")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")


@app.route("/api/v1/config", methods=["GET", "POST"])
def handle_config():
    global config
    if request.method == "GET":
        return jsonify(config)
    data = request.json
    config.update(data)
    return jsonify({"status": "ok", "config": config})


@app.route("/api/v1/models", methods=["GET", "POST"])
def get_models():
    api_key = config.get("api_key")
    if request.method == "POST":
        data = request.get_json() or {}
        api_key = data.get("api_key", config.get("api_key"))

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    headers["Content-Type"] = "application/json"

    try:
        response = requests.get(
            f"{config['base_url']}/models", headers=headers, timeout=30
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


@app.route("/api/v1/ui-config", methods=["GET"])
def get_ui_config():
    test_set_dir = get_test_set_dir()
    ui_json_path = os.path.join(test_set_dir, "UI.json")
    ui_config = load_json(ui_json_path)
    if ui_config:
        return jsonify(ui_config)
    return jsonify({"formatGroups": []})


@app.route("/api/v1/system-prompts", methods=["GET"])
def get_system_prompts():
    test_set_dir = get_test_set_dir()
    prompts = []
    if os.path.exists(test_set_dir):
        for f in os.listdir(test_set_dir):
            if f.endswith((".txt", ".md")):
                filepath = os.path.join(test_set_dir, f)
                content = read_file(filepath)
                prompts.append({"name": f, "path": filepath, "content": content or ""})
    return jsonify(prompts)


@app.route("/api/v1/question-groups", methods=["GET"])
def get_question_groups():
    test_set_dir = get_test_set_dir()
    questions_dir = os.path.join(test_set_dir, config.get("questions_dir", "questions"))
    groups = {}
    if os.path.exists(questions_dir):
        for f in os.listdir(questions_dir):
            if f.endswith(".json"):
                filepath = os.path.join(questions_dir, f)
                data = load_json(filepath)
                if data:
                    group_name = f.replace(".json", "")
                    questions = []
                    for q in data.get("questions", []):
                        questions.append(
                            {
                                "id": q.get("id", ""),
                                "question": q.get("question", ""),
                                "expected_answer": q.get("expected_answer", ""),
                            }
                        )
                    groups[group_name] = {
                        "name": group_name,
                        "file": f,
                        "path": filepath,
                        "questions": questions,
                    }
    return jsonify(groups)


@app.route("/api/v1/bindings", methods=["GET", "POST"])
def handle_bindings():
    global bindings
    test_set_dir = get_test_set_dir()
    bindings_file = os.path.join(
        test_set_dir, config.get("bindings_file", "bindings.json")
    )

    if request.method == "GET":
        bindings = load_json(bindings_file) or {}
        return jsonify(bindings)

    data = request.json or {}
    bindings = data.get("bindings", {})
    save_json(bindings_file, bindings)
    return jsonify({"status": "ok", "bindings": bindings})


@app.route("/api/v1/results", methods=["GET"])
def get_all_results():
    results = {}
    if os.path.exists(RESULTS_DIR):
        for f in os.listdir(RESULTS_DIR):
            if f.endswith(".json"):
                key = f.replace(".json", "")
                results[key] = load_json(os.path.join(RESULTS_DIR, f))
    return jsonify(results)


@app.route("/api/v1/answer-cache", methods=["GET"])
def get_answer_cache():
    cache = {}
    if os.path.exists(ANSWER_CACHE_DIR):
        for f in os.listdir(ANSWER_CACHE_DIR):
            if f.endswith(".json"):
                key = f.replace(".json", "")
                cache[key] = load_json(os.path.join(ANSWER_CACHE_DIR, f))
    return jsonify(cache)


@app.route("/api/v1/clear-results", methods=["POST"])
def clear_results():
    if os.path.exists(RESULTS_DIR):
        for f in os.listdir(RESULTS_DIR):
            if f.endswith(".json"):
                os.remove(os.path.join(RESULTS_DIR, f))
    return jsonify({"status": "ok"})


@app.route("/api/v1/stop-tests", methods=["POST"])
def stop_tests():
    config["stop_flag"] = True
    return jsonify({"status": "ok"})


def call_ai(system_prompt, user_prompt, model=None, max_retries=None):
    if max_retries is None:
        max_retries = config.get("max_retries", 3)

    headers = {}
    if config.get("api_key"):
        headers["Authorization"] = f"Bearer {config['api_key']}"
    headers["Content-Type"] = "application/json"

    payload = {
        "model": model or config["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": config.get("temperature", 0.7),
        "top_p": config.get("top_p", 1.0),
    }

    if config.get("top_k"):
        payload["top_k"] = config["top_k"]
    if config.get("min_p"):
        payload["min_p"] = config["min_p"]
    context_size = config.get("context_size")
    if context_size is not None and context_size > 0:
        payload["context_size"] = context_size

    for attempt in range(max_retries):
        if config.get("stop_flag"):
            return None
        try:
            response = requests.post(
                f"{config['base_url']}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            if response.status_code == 200:
                result = response.json()
                if result.get("choices") and result["choices"][0].get("message"):
                    content = result["choices"][0]["message"].get("content")
                    if content:
                        return content
                log_debug(f"AI返回为空，attempt={attempt}, response={result}")
            elif response.status_code == 429:
                time.sleep(2**attempt)
            else:
                log_debug(
                    f"AI请求失败，status={response.status_code}, response={response.text}"
                )
                time.sleep(1)
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            time.sleep(2**attempt)
    return None


def run_single_test(test_item, source_content, group_name, model):
    if config.get("stop_flag"):
        return None

    test_id = test_item.get("id", "")
    question = test_item.get("question", "")
    answer = test_item.get("answer", "")
    source = test_item.get("source", "")

    system_prompt = f"以下是被测试的文件内容：\n\n{source_content}\n\n请根据以上文件内容回答用户的问题。"
    user_prompt = question

    test_count = config.get("test_count", 1)
    multi_answers = []

    for i in range(test_count):
        if config.get("stop_flag"):
            break
        ai_answer = call_ai(system_prompt, user_prompt, model=model)
        if ai_answer:
            multi_answers.append(
                {"index": i + 1, "answer": ai_answer, "timestamp": time.time()}
            )

    result = {
        "id": test_id,
        "question": question,
        "expected_answer": answer,
        "multi_answers": multi_answers,
        "model": model,
        "group": group_name,
        "source": source,
    }

    return result


@app.route("/api/v1/run-tests", methods=["POST"])
def run_tests():
    config["stop_flag"] = False
    data = request.json
    test_files = data.get("test_files", [])
    models = data.get("models", [config.get("model", "gpt-4o")])

    if not test_files:
        return jsonify({"error": "No test files specified"}), 400

    test_set_dir = get_test_set_dir()

    ui_json_path = os.path.join(test_set_dir, "UI.json")
    ui_config = load_json(ui_json_path)

    if not ui_config:
        return jsonify({"error": "UI.json not found"}), 400

    format_groups = ui_config.get("formatGroups", [])
    file_to_group = {}
    for group in format_groups:
        for f in group.get("files", []):
            key = f"{f.get('source')}|{f.get('testQuestion')}"
            file_to_group[key] = group.get("name", "default")

    all_results = {}
    source_content_cache = {}

    def generate():
        total_tasks = 0
        completed_tasks = 0

        for file_key in test_files:
            yield f"data: {json.dumps({'type': 'status', 'message': f'加载测试文件: {file_key.split('/').pop()}'})}\n\n"

            parts = file_key.split("|")
            if len(parts) != 2:
                continue

            source = parts[0]
            test_question = parts[1]

            if source not in source_content_cache:
                source_rel = source.replace("测试集/", "").replace("测试集\\", "")
                source_path = os.path.join(test_set_dir, source_rel)
                content = read_file(source_path)
                source_content_cache[source] = content if content else ""

            source_content = source_content_cache.get(source, "")

            question_base = test_question.replace("测试集/", "").replace("测试集\\", "")
            abs_question_dir = os.path.join(test_set_dir, question_base)

            test_items = []
            if os.path.exists(abs_question_dir):
                for item in os.listdir(abs_question_dir):
                    item_path = os.path.join(abs_question_dir, item)
                    if os.path.isdir(item_path) and item.startswith("问题"):
                        question_subdir = os.path.join(item_path, "问题")
                        answer_subdir = os.path.join(item_path, "答案")

                        if os.path.exists(question_subdir) and os.path.exists(
                            answer_subdir
                        ):
                            json_files = os.listdir(question_subdir)
                            answer_files = os.listdir(answer_subdir)

                            for qf in json_files:
                                if not qf.endswith(".json"):
                                    continue

                                qf_full_path = os.path.join(question_subdir, qf)
                                base_name = qf.replace("答案", "")
                                matching_af = None
                                for af in answer_files:
                                    if af.replace(".json", "") == base_name.replace(
                                        ".json", ""
                                    ):
                                        matching_af = af
                                        break

                                if matching_af:
                                    question_data = load_json(qf_full_path)
                                    answer_json_path = os.path.join(
                                        answer_subdir, matching_af
                                    )
                                    answer_data = load_json(answer_json_path)

                                    if question_data and answer_data:
                                        test_items.append(
                                            {
                                                "id": question_data.get("id"),
                                                "question": question_data.get(
                                                    "question"
                                                ),
                                                "answer": answer_data.get("answer"),
                                                "source": source,
                                                "testQuestion": test_question,
                                            }
                                        )

            if not test_items:
                continue

            total_tasks += len(test_items)
            group_name = file_to_group.get(file_key, "default")

            for model in models:
                group_key = f"{group_name}_{model}"

                if group_key not in all_results:
                    all_results[group_key] = []

                yield f"data: {json.dumps({'type': 'status', 'message': f'开始测试 {group_key}，共 {len(test_items)} 题'})}\n\n"

                for item in test_items:
                    if config.get("stop_flag"):
                        yield f"data: {json.dumps({'type': 'status', 'message': '测试已终止'})}\n\n"
                        return

                    result = run_single_test(item, source_content, group_name, model)
                    all_results[group_key].append(result)
                    completed_tasks += 1

                    first_answer = ""
                    if result.get("multi_answers"):
                        first_answer = result["multi_answers"][0].get("answer", "")

                    yield f"data: {
                        json.dumps(
                            {
                                'type': 'result',
                                'group': group_key,
                                'id': result.get('id'),
                                'question': result.get('question', ''),
                                'expected_answer': result.get('expected_answer', ''),
                                'ai_answer': first_answer,
                                'multi_answers': result.get('multi_answers', []),
                                'test_count': len(result.get('multi_answers', [])),
                                'source': result.get('source', ''),
                                'model': result.get('model', ''),
                                'completed': completed_tasks,
                                'total': total_tasks,
                            },
                            ensure_ascii=False,
                        )
                    }\n\n"

        yield f"data: {json.dumps({'type': 'done', 'message': '测试完成'})}\n\n"

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    for dir_path in [DATA_DIR, TESTS_DIR, SRC_DIR, RESULTS_DIR, ANSWER_CACHE_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    app.run(debug=True, port=5000)
