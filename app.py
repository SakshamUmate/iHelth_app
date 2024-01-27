""" 
  importing all the modules that is needed below here

"""
from pymed import PubMed
from typing import List
from haystack import component
from haystack import Document
from haystack.components.generators import HuggingFaceTGIGenerator
from dotenv import load_dotenv
import os 
from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
import gradio as gr
import time



""" 

  loading env file and getting hugging face api key for credential logging and fetching information

"""
load_dotenv()
os.environ['HUGGINGFACE_API_KEY'] = os.getenv('HUGGINGFACE_API_KEY')

""" 
  pubmed is an open source library which contains vector database for medical related data
  it consists of research paper , medicine and disease data's eigen vector pretrained.
"""
pubmed = PubMed(tool="Haystack2.0Prototype", email="coderayush1010@gmail.com")

def documentize(article):
  return Document(content=article.abstract, meta={'title': article.title, 'keywords': article.keywords})


""" 
    this class fetches information from pubmed for any given queries
    which is further processes by the llm model 

"""

@component
class PubMedFetcher():

  @component.output_types(articles=List[Document])
  def run(self, queries: list[str]):
    cleaned_queries = queries[0].strip().split('\n')

    articles = []
    try:
      for query in cleaned_queries:
        response = pubmed.query(query, max_results = 1)
        documents = [documentize(article) for article in response]
        articles.extend(documents)
    except Exception as e:
        print(e)
        print(f"Couldn't fetch articles for queries: {queries}" )
    results = {'articles': articles}
    return results

keyword_llm = HuggingFaceTGIGenerator("mistralai/Mixtral-8x7B-Instruct-v0.1")
keyword_llm.warm_up()

llm = HuggingFaceTGIGenerator("mistralai/Mixtral-8x7B-Instruct-v0.1")
llm.warm_up()



""" 

template for llm in which it willl process the queries and convert it into 
below format.

"""


keyword_prompt_template = """
Your task is to convert the following question into 3 keywords that can be used to find relevant medical research papers on PubMed.
Here is an examples:
question: "What are the latest treatments for major depressive disorder?"
keywords:
Antidepressive Agents
Depressive Disorder, Major
Treatment-Resistant depression
---
question: {{ question }}
keywords:
"""

"""
for geeting better result give better promts
"""

prompt_template = """
Answer the question truthfully based on the given documents.
If the documents don't contain an answer, use your existing knowledge base and give comprehensive answer make bullets points if possible.

q: {{ question }}
Articles:
{% for article in articles %}
  {{article.content}}
  keywords: {{article.meta['keywords']}}
  title: {{article.meta['title']}}
{% endfor %}

"""


"""
  setting up promptimg templates
"""
keyword_prompt_builder = PromptBuilder(template=keyword_prompt_template)

prompt_builder = PromptBuilder(template=prompt_template)
fetcher = PubMedFetcher()


"""
  building pipeline for the whole Architecture.
  Architecture is give on github page.
"""

pipe = Pipeline()

pipe.add_component("keyword_prompt_builder", keyword_prompt_builder)
pipe.add_component("keyword_llm", keyword_llm)
pipe.add_component("pubmed_fetcher", fetcher)
pipe.add_component("prompt_builder", prompt_builder)
pipe.add_component("llm", llm)

pipe.connect("keyword_prompt_builder.prompt", "keyword_llm.prompt")
pipe.connect("keyword_llm.replies", "pubmed_fetcher.queries")

pipe.connect("pubmed_fetcher.articles", "prompt_builder.articles")
pipe.connect("prompt_builder.prompt", "llm.prompt")

def ask(question):      
    output = pipe.run(data={"keyword_prompt_builder":{"question":question},
                            "prompt_builder":{"question": question},
                            "llm":{"generation_kwargs": {"max_new_tokens": 800}}})
    print(question)
    print(output['llm']['replies'][0])
    return output['llm']['replies'][0] 


    """
    for testing purpose only
    """
# iface = gr.Interface(fn=ask, inputs=gr.Textbox(
#         value="How are mRNA vaccines being used for cancer treatment?"), 
#             outputs="markdown",  
#             title="LLM Augmented Q&A over PubMed Search Engine",
#             description="Ask a question about BioMedical and get an answer from a friendly AI assistant.",
#             examples=[["How are mRNA vaccines being used for cancer treatment?"], 
#                     ["Give me a case study on Cancer diseas."],
#                     ["Suggest me some Case Studies related to Pneumonia."],
#                     ["Tell me about HIV AIDS."],["Suggest some case studies related to Auto Immune Disorders."],
#                     ["How to treat a COVID infected Patient?"]],
#         theme=gr.themes.Soft(),
#         allow_flagging="never",)


# iface.launch(debug=True)

# if __name__ == '__main__':
#    str = "Give me a case study on Cancer diseas."
#    ask(str)

