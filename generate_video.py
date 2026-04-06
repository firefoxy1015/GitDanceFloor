"""
GitDanceFloor - Veo 3 Video Generation via Google Flow
使用 Google Veo 3 (Flow) 為舞池項目生成宣傳視頻

用法:
    export GOOGLE_API_KEY="your_api_key_here"
    python3 generate_video.py

或指定自定義提示詞:
    python3 generate_video.py --prompt "your custom prompt"
    python3 generate_video.py --output my_video.mp4
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import urllib.error

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.0-generate-001"

DEFAULT_PROMPT = (
    "A vibrant, energetic dance floor scene with multiple diverse 3D animated characters "
    "performing different styles of dance simultaneously — hip hop, breakdance, thriller, "
    "twerk, swing, and silly dancing. The dancers are illuminated by colorful dynamic stage "
    "lighting with rhythmic music beats. The camera sweeps across the dance floor in a "
    "cinematic wide-angle shot, capturing the synchronized choreography. "
    "High quality, cinematic, 4K, dance party atmosphere."
)


def _api_request(method: str, url: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {error_body}") from e


def submit_video_generation(api_key: str, prompt: str) -> str:
    """提交 Veo 3 視頻生成請求，返回 operation name。"""
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning?key={api_key}"
    body = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "aspectRatio": "16:9",
            "sampleCount": 1,
        },
    }
    response = _api_request("POST", url, body)
    operation_name = response.get("name")
    if not operation_name:
        raise RuntimeError(f"未收到 operation name: {response}")
    return operation_name


def poll_operation(api_key: str, operation_name: str, poll_interval: int = 15) -> dict:
    """輪詢操作狀態直到完成，返回最終響應。"""
    url = f"{BASE_URL}/{operation_name}?key={api_key}"
    while True:
        response = _api_request("GET", url, None)
        if response.get("done"):
            return response
        print("      仍在生成中...", flush=True)
        time.sleep(poll_interval)


def download_video(video_uri: str, api_key: str, output_path: str) -> None:
    """從 Google AI 文件服務下載視頻。"""
    # 若是 Google AI files URI，轉換為可下載的 URL
    if video_uri.startswith("https://"):
        download_url = video_uri
    else:
        # 格式: files/{file_id}
        file_id = video_uri.split("/")[-1]
        download_url = f"{BASE_URL}/files/{file_id}?alt=media&key={api_key}"

    req = urllib.request.Request(download_url)
    with urllib.request.urlopen(req) as resp, open(output_path, "wb") as f:
        f.write(resp.read())


def generate_video(api_key: str, prompt: str, output_path: str = "dance_floor_video.mp4") -> str:
    """
    使用 Google Veo 3 (Flow) 生成視頻並保存到本地。

    Args:
        api_key:     Google AI API 密鑰（從 https://aistudio.google.com/apikey 獲取）
        prompt:      視頻生成提示詞
        output_path: 輸出視頻文件路徑

    Returns:
        生成的視頻文件路徑
    """
    print(f"[1/3] 提交視頻生成請求...")
    print(f"      模型: {MODEL}")
    print(f"      提示詞: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

    operation_name = submit_video_generation(api_key, prompt)
    print(f"      操作 ID: {operation_name}")

    print(f"\n[2/3] 等待 Veo 3 生成視頻（通常需要 2-5 分鐘）...")
    result = poll_operation(api_key, operation_name)

    # 從響應中取出視頻 URI
    try:
        predictions = result["response"]["predictions"]
        video_uri = predictions[0]["bytesBase64Encoded"]
        is_base64 = True
    except (KeyError, IndexError):
        is_base64 = False
        try:
            video_uri = result["response"]["videos"][0]["uri"]
        except (KeyError, IndexError):
            raise RuntimeError(f"無法從響應中解析視頻: {json.dumps(result, indent=2)}")

    print(f"\n[3/3] 保存視頻到 {output_path}...")
    if is_base64:
        import base64
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(video_uri))
    else:
        download_video(video_uri, api_key, output_path)

    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n✓ 視頻已保存: {output_path} ({file_size_mb:.1f} MB)")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="使用 Google Veo 3 (Flow) 為 GitDanceFloor 項目生成視頻",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  export GOOGLE_API_KEY='AIza...'
  python3 generate_video.py
  python3 generate_video.py --prompt "dancers on a neon-lit stage"
  python3 generate_video.py --output promo.mp4

獲取 API 密鑰: https://aistudio.google.com/apikey
        """,
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="視頻生成提示詞（默認使用 GitDanceFloor 舞池場景描述）",
    )
    parser.add_argument(
        "--output",
        default="dance_floor_video.mp4",
        help="輸出視頻文件路徑（默認: dance_floor_video.mp4）",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("GOOGLE_API_KEY"),
        help="Google AI API 密鑰（也可通過 GOOGLE_API_KEY 環境變量設置）",
    )
    args = parser.parse_args()

    if not args.api_key:
        print("錯誤: 請提供 Google AI API 密鑰。")
        print()
        print("  方法 1（推薦）: export GOOGLE_API_KEY='your_key_here'")
        print("  方法 2:         python3 generate_video.py --api-key 'your_key_here'")
        print()
        print("  從 Google AI Studio 獲取免費密鑰:")
        print("  https://aistudio.google.com/apikey")
        sys.exit(1)

    try:
        generate_video(
            api_key=args.api_key,
            prompt=args.prompt,
            output_path=args.output,
        )
    except RuntimeError as e:
        print(f"\n錯誤: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
