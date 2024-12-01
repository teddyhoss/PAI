import os
from toolhouse import Toolhouse
from groq import Groq

# API Keys (In production, these should be environment variables)
os.environ['GROQ_API_KEY'] = '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'
TOOLHOUSE_KEY = 'th-tmKDVLNhiv0uXzH5CKMDZaZTqi57fWexf61FD9KaD14'

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# Initialize Toolhouse with API key
th = Toolhouse(api_key=TOOLHOUSE_KEY)

# Modified prompt for Italian schools dashboard
messages = [{
    "role": "user",
    "content": "mandami via mail alla mail francesco.sabbarese97@gmail.com la parola ciao"
}]

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=th.get_tools(),
)

# Run tools and get results
tool_run = th.run_tools(response)
messages.extend(tool_run)

# Get final response
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=th.get_tools(),
)

print(response.choices[0].message.content)