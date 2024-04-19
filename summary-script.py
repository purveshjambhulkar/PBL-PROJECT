from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

ARTICLE = """
So currently I am pursuing Bachelor of Engineering (B.E.) in D.Y. Patil College of Engineering Akurdi, Pune.

I want to become a Data Scientist or a Fullstack Developer.I also have a keen interest in Cybersecurity and Networking.

I can code efficiently in Python knows the basics of Flask and for Web Development and I prefer using Bootstrap.I am capable of Working with various powerful modules in Python such as Selenium, Pandas, SMTPlib etc.
"""
print(summarizer(ARTICLE, max_length=50, min_length=30, do_sample=False))
#
#
# from transformers import AutoModelForCausalLM, AutoTokenizer
#
# model_id = "mistral-community/Mixtral-8x22B-v0.1"
# tokenizer = AutoTokenizer.from_pretrained(model_id)
#
# model = AutoModelForCausalLM.from_pretrained(model_id)
#
# text = "Hello my name is"
# inputs = tokenizer(text, return_tensors="pt")
#
# outputs = model.generate(**inputs, max_new_tokens=20)
# print(tokenizer.decode(outputs[0], skip_special_tokens=True))