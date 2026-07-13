# FormTest - AI構造化フォーマット解析能力テストフレームワーク

> **付属のテストセットはすべてAIが生成した架空のデータであり、実際のデータではありません。万が一、実在のものと一致した場合は、完全に偶然です。**
>
> **本プロジェクトは十分なプログラム構築とテスト計画を経ていません。コード構造とテストカバレッジはまだ不完全であり、参考および学習目的でのみ提供されています。**

大規模言語モデル（LLM）の構造化データフォーマットの理解・解析能力を評価するための自動テストフレームワークです。事前定義されたテストケースを使用して、AI APIを自動的に呼び出し、返された結果と期待される回答を比較することで、モデルのフォーマット理解性能を定量的に測定します。

## クイックスタート

### 1. 依存関係のインストール

```bash
pip install -r APPs/requirements.txt
```

### 2. 起動

```bash
cd APPs
python app.py
# または run.bat をダブルクリック
```

ブラウザで開く [http://localhost:5000](http://localhost:5000)

### 3. 設定

起動後、Webページ右上隅の **設定** ボタンをクリックし、APIアドレス、モデル、パラメーターなどを設定します。`APPs/config.example.json` を参考にして設定ファイルを作成することもできます。

主な設定項目：
- `base_url` — APIアドレス（自動で `/v1` を追加可能）
- `model` — デフォルトのモデル名
- `model_thinking_config` — モデルごとの思考/推論モード設定
- `streaming` — SSEストリーミング出力のオン/オフ
- `concurrency` — 並行スレッド数
- `disabled_params` — フロントエンドで非表示/無効にするパラメーター

### 4. テストの実行

1. **キャンバス**上でノードエディターを使用して組み合わせを作成：プロンプト × 質問 × モデル
2. **テスト開始**をクリックしてストリーミング結果をリアルタイムで表示
3. テスト完了後は **結果履歴** で確認/フィルタリング

## プロジェクト構造

```
FormTest/
├── APPs/                          # メインプログラム
│   ├── app.py                     # Flaskバックエンド（API + テスト実行エンジン + SSEストリーミング）
│   ├── requirements.txt           # Python依存関係
│   ├── run.bat                    # Windows起動スクリプト
│   ├── config.example.json        # 設定テンプレート
│   ├── flow.json                  # フローチャート定義
│   └── static/
│       └── index.html             # フロントエンドSPA（ネイティブHTML/CSS/JS、約7300行）
├── Benches/                       # テストデータセット
│   ├── AI嘉豪测试/                # AIリテラシー選択問題（NAGI STUDIOより改変）
│   ├── Python测试/                # Python発展知識テスト
│   ├── 企业信息测试/              # 架空企業の工商情報
│   ├── 教学视频测试/              # Python入門教学ビデオ内容
│   └── 运行日志测试/              # システム運用ログ分析
├── skills/                        # ユーザーが直接使用可能なツールスクリプト
│   ├── New-TestSet-新建测试集.ps1 # 新規テストセットの骨格を作成するPowerShellスクリプト
│   └── QA-Extract-问答提取.md     # ソースファイルからQAペアを抽出するガイド
├── .opencode/
│   └── skills/                    # opencode AIスキル（AI Agentサポート用）
│       ├── new-test-set/          # テストセット骨格作成
│       └── qa-extract/            # QAペア抽出
├── .gitignore
├── LICENSE                        # Apache License 2.0
└── README.md                      # 本ファイル
```

## テストセット

### 構造

各テストセットは `.test-set-part` マーカーファイルを通じてサブディレクトリの役割を識別します。ディレクトリ名は任意で、システムはマーカーファイルの内容で役割を識別します：

```
Benches/<名前>/
├── <質問ディレクトリ>/              # .test-set-part → "questions" を含む
│   ├── .test-set-part
│   ├── 基础问题.json                # 10問
│   └── 进阶问题.json                # 10問（一部のテストセットは基礎問題のみ）
├── <プロンプトディレクトリ>/         # .test-set-part → "prompts" を含む
│   ├── .test-set-part
│   ├── <名前>原版.json              # プレーンテキスト記述形式
│   ├── <名前>列表.json              # 番号付きリスト形式
│   ├── <名前>JSON.json              # JSON構造化形式
│   ├── <名前>YAML.json              # YAML形式
│   ├── <名前>XML.json               # XML形式
│   ├── <名前>Markdown.json          # Markdownテーブル形式
│   ├── <名前>MarkdownKV.json        # Markdownキー・バリュー形式
│   └── <名前>DSL.json               # カスタムDSL形式
└── <結果ディレクトリ>/              # .test-set-part → "results" を含む（実行時に生成）
    └── .test-set-part
```

### テスト形式

| 形式 | 説明 |
|------|------|
| 原版 (Plain Text) | プレーンテキスト記述、ベースラインとして使用 |
| リスト (List) | 番号付き/箇条書きリスト |
| JSON | 標準JSONオブジェクト |
| YAML | YAML構造化データ |
| XML | XMLタグ階層表現 |
| Markdown | Markdownテーブル |
| MarkdownKV | Markdownキー・バリューペア |
| DSL | カスタムドメイン特化言語 |

### テストドメイン

| テストセット | 内容ドメイン | 問題数 | 出典 |
|--------|----------|------|------|
| 教学视频テスト | Pythonプログラミング講座の書き起こし | 20 | AI生成の架空データ |
| 企业信息テスト | 架空企業の工商情報 | 20 | AI生成の架空データ |
| 运行日志テスト | システム運用ログエントリ | 20 | AI生成の架空データ |
| Pythonテスト | Pythonデコレータ/ジェネレータ/コンテキストマネージャ | 20 | AI生成の架空データ |
| AIリテラシーテスト | AIリテラシー選択問題（基礎/発展/誤解/人文） | 30 | [NAGI STUDIO](https://github.com/nagi-studio/ai-jiahao) (MIT) より改変 |

## 主な機能

- **ビジュアルキャンバスエディター** — SVGノードキャンバス、ドラッグ＆ドロップでプロンプト × 質問 × モデルを組み合わせ、接続線の描画に対応
- **元に戻す/やり直し** — 完全な履歴システム、Ctrl+Z / Ctrl+Shift+Z 対応
- **マルチフォーマット比較テスト** — 同じ内容を8種類の形式で提示し、各形式に対するモデルの理解度の差異を評価
- **バッチ自動テスト** — プロンプト × 質問 × モデルのデカルト積組み合わせ、自動並行実行
- **マルチモデル管理** — モデルポップアップ管理、追加モデルの追加/削除/並び替えに対応
- **推論設定** — モデルごとに thinking/reasoning_effort パラメーターを個別設定
- **パラメーター無効化トグル** — 各パラメーターを dot-toggle で個別に有効/無効化
- **ストリーミングリアルタイム出力** — SSEベースのストリーミング結果プッシュ、テスト進捗をリアルタイム表示
- **結果履歴の表示** — ステータス/モデル/テキストで過去の実行結果を検索・フィルタリング
- **アーカイブ/復元** — テスト設定のスナップショットを保存/読み込み（キャンバス状態 + モデル推論設定を含む）
- **_notFound モデル検出** — キャンバスが利用不可のモデルを自動検出し⚠警告を表示
- **自動 /v1 補完** — トグルスイッチでAPIアドレスに自動的に `/v1` を追加
- **ダーク/ライトテーマ** — 完全なCSS変数システムによるテーマ切り替え対応
- **Anthropic API対応** — Anthropicメッセージ形式 + 専用SSE推論解析に対応
- **複数回テスト** — 同一質問を繰り返し実行し、回答の安定性を測定
- **並行制御** — 設定可能な並行スレッド数とリトライ戦略
- **インクリメンタル保存** — テスト中に定期的に結果を増分保存し、偶発的な損失を防止
- **パス安全性検証** — パストラバーサル攻撃の防止、Windows予約名チェック、ファイル名ホワイトリスト

## API インターフェース

| エンドポイント | メソッド | 説明 |
|------|------|------|
| `/` | GET | フロントエンドSPAを提供 |
| `/api/v1/config` | GET/POST | 設定の読み取り/保存 |
| `/api/v1/models` | GET/POST | 利用可能なモデル一覧の取得/保存 |
| `/api/v1/test-set/scan` | GET | テストセットのスキャン |
| `/api/v1/test-set/prompts` | GET | テストセットのシステムプロンプトを取得 |
| `/api/v1/test-set/questions` | GET | テストセットの質問を取得 |
| `/api/v1/test-set/results` | GET | 過去のテスト結果を取得 |
| `/api/v1/test-job/hub` | POST | 統一タスクスケジューリング（action: start/status/stop） |
| `/api/v1/test-job/stream/<job_id>` | GET | SSEストリーミングリアルタイム結果プッシュ |
| `/api/v1/canvas-state` | GET/POST | キャンバス状態の保存/読み取り |
| `/api/v1/archives` | GET/POST/DELETE | アーカイブ管理 |
| `/api/v1/tags` | GET | すべてのタグを取得 |

エラー応答：`404` → `{"error": "Not found"}`、`500` → `{"error": "服务器内部错误"}`

## 設定項目

| キー | 型 | 説明 |
|-----|------|------|
| `api_key` | string | APIキー |
| `base_url` | string | APIアドレス |
| `model` | string | デフォルトモデル名 |
| `models` | string[] | 追加モデル一覧 |
| `temperature` | float | 温度 (0-2) |
| `top_p` | float | Top-P (0-1) |
| `top_k` | int | Top-K |
| `min_p` | float | Min-P |
| `context_size` | int | コンテキストサイズ |
| `concurrency` | int | 並行スレッド数 (1-50) |
| `test_count` | int | 質問ごとの繰り返しテスト回数 |
| `max_retries` | int | 最大リトライ回数 |
| `streaming` | bool | SSEストリーミングのオン/オフ |
| `timeout` | int | リクエストタイムアウト秒数 |
| `model_thinking_config` | object | モデルごとの推論設定、例：`{"model-a": {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}}` |
| `anthropic_mode` | bool | Anthropicメッセージ形式を強制使用 |
| `force_openai_endpoint` | bool | OpenAI互換エンドポイントを強制使用 |
| `disabled_params` | string[] | フロントエンドで非表示/無効にするパラメーター名のリスト |

## OpenCode スキル

このプロジェクトには、テストセットを迅速に作成・管理するための2つのツールスキルが含まれています：

### ユーザーツール（`skills/`）

開発者が直接実行可能なスクリプトとドキュメント：

| ファイル | 説明 |
|------|------|
| `skills/New-TestSet-新建测试集.ps1` | PowerShellスクリプト。番号付きテストセットの骨格ディレクトリと .test-set-part マーカーファイルを自動作成 |
| `skills/QA-Extract-问答提取.md` | ソースファイルからQAペアを抽出し、互換性のあるJSONファイルを生成する方法を説明する詳細ガイド |

### AI Agent スキル（`.opencode/skills/`）

[opencode](https://opencode.ai) または互換性のあるAIコーディングツールを使用している場合、`.opencode/skills/` 以下のスキルがAI Agentによって自動的に検出・ロードされます：

| スキル | 説明 |
|------|------|
| `new-test-set` | AIがテストセットの骨格（ディレクトリ + マーカーファイル）を作成するようガイド。自動番号付けで衝突を回避 |
| `qa-extract` | AIがソースファイルからQAペアを抽出するようガイド。出力形式はFormTestテストセット互換のJSON |

## 技術スタック

- **バックエンド**: Python Flask + Flask-CORS
- **フロントエンド**: ネイティブHTML / CSS（カスタム変数システム、ダーク/ライトテーマ）/ JavaScript
- **AI呼び出し**: `requests` ライブラリ（SSEストリーミングと通常JSONの両モード対応、OpenAPI / Anthropic API互換）
- **並行処理**: `ThreadPoolExecutor` スレッドプール + 指数バックオフリトライ
- **出力**: Server-Sent Events（`text/event-stream`）

## 重要なお知らせ

**本プロジェクトのテストセット内容はすべてAIが生成した架空のサンプルデータであり、実際のデータではありません。万が一、実在のものと一致した場合は、完全に偶然です。** すべてのデータはAIモデルの構造化フォーマットの理解・解析能力を評価するためだけのものであり、実際のビジネスシナリオやエンティティを代表するものではありません。

- `Benches/AI嘉豪测试/` は [NAGI STUDIO の AI リテラシーテスト](https://github.com/nagi-studio/ai-jiahao) を改変したもので、MITライセンスの下で公開されています
- その他のテストセットはすべてAIが生成した架空のデータです

## ライセンス

Apache License 2.0 — 詳細は [LICENSE](LICENSE) ファイルを参照

---

**これはAIが粗悪な酒を飲んで書いたようなものかもしれません — 私の本業はAIをとことん試すことです。**
