from app.services.batch.batch_response_parser import (
    BatchResponseParser,
)

response = """
{
    "version":1,
    "blocks":[
        {
            "id":9,
            "status":"updated",
            "text":"Developed scalable REST APIs using Spring Boot."
        },
        {
            "id":10,
            "status":"unchanged",
            "text":"Implemented REST APIs."
        }
    ]
}
"""

data = BatchResponseParser.parse(response)

print("=" * 60)

print(data)