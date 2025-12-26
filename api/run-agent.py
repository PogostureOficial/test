from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def handler(request):
    try:
        body = json.loads(request.body)
        task = body.get("task", "")

        response = client.responses.create(
            model="gpt-4.1",
            tools=[
                {
                    "type": "computer",
                    "browser": "chromium",
                    "display_width": 1280,
                    "display_height": 800
                }
            ],
            input=[
                {
                    "role": "user",
                    "content": f"""
Realizá esta tarea paso a paso.
Después de cada acción importante:
- sacá una captura
- indicá la pestaña activa
- describí el movimiento del cursor

Tarea: {task}
"""
                }
            ]
        )

        screenshots = []
        for item in response.output:
            for content in item.get("content", []):
                if content.get("type") == "output_image":
                    screenshots.append(content["image_url"])

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({
                "success": True,
                "logs": response.output_text,
                "screenshots": screenshots
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) })
        }
