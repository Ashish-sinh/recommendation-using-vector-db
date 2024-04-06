import streamlit as st 
import pandas as pd 
import os 
from qdrant_client import QdrantClient , models 
from langchain.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings 
from dotenv import load_dotenv 
load_dotenv()

hugginface_api_key = os.environ['HUGGINGFACEHUB_API_TOKEN']
qdrant_api_key  = os.environ['QDRANT_API_KEY']

st.set_page_config(
    page_title=' Fashion Recommendation System',
    page_icon = '🛒'
)

st.title('🛒🛍️  Fashion Recommendation System')
st.title('')

df = pd.read_csv('fas.csv')


collection_name = 'fashion-recommendation'

client = QdrantClient(
    url="https://3e9ea0c2-1b73-44e6-a03c-31bd5c5cd570.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key=qdrant_api_key, ) 

embeddings = HuggingFaceInferenceAPIEmbeddings ( model_name = 'sentence-transformers/all-MiniLM-L6-v2' , 
                                                 api_key = hugginface_api_key ) 



with st.sidebar : 
    st.title('🛍️ Fashion Recommendation System 🛒✨') 
    st.image('https://emerj.com/wp-content/uploads/2018/10/recommendation-engines-for-fashion-6-current-applications-6.jpg') 
    st.write('* :green[Discover your perfect look with our fashion recommendation system!] 👗 \n * :green[Our AI suggests outfits and accessories based on your interests, keeping you stylish and confident.] 💫 \n * :green[Let technology upgrade your wardrobe effortlessly! 🛍️] ')
    st.link_button('GitHub SourceCode',url = 'https://github.com/Ashish-sinh/recommendation-using-vector-db')
        

selected_product = st.selectbox(':black[Please Select  Product]' ,df['ProductName']) 
st.subheader('')
input_text = st.text_input(':black[Please Enter Your Intrest]') 


col1 , col2 = st.columns(2) 

with col1  : 
    if st.button('Show Recommendation Releted to Input Text') :

        with st.spinner("Processing...") :
            embed = list(embeddings.embed_query(input_text))
            hits = client.search ( 
                collection_name= collection_name,
                query_vector= embed , 
                limit= 5 , ) 

        for hit in hits:
            st.write('* {} :green[score ]: :red[{:.2f}]'.format(hit.payload['ProductName'] , hit.score))

with col2  : 
    if st.button('Show Recommendation Releted to Product') :

        with st.spinner("Processing...") :
            embed = list(embeddings.embed_query(selected_product))
            hits = client.search ( 
                collection_name= collection_name,
                query_vector= embed , 
                limit= 5 , ) 

        for hit in hits:
            st.write('* {} :green[score ]: :red[{:.2f}]'.format(hit.payload['ProductName'] , hit.score))
