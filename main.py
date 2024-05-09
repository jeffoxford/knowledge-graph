import streamlit as st
from googleapiclient.discovery import build

def query_knowledge_graph(query):
    service = build("kgsearch", "v1", developerKey=api_key)
    response = service.entities().search(query=query, limit=5).execute()
    return response

# Streamlit interface
st.title("Google Knowledge Graph Search Tool")

# User input
entity_name = st.text_input("Enter the name of an entity:", "")

if entity_name:
    # Query the Knowledge Graph API
    result = query_knowledge_graph(entity_name)

    if 'itemListElement' in result:
        for element in result['itemListElement']:
            entity = element.get('result', {})
            st.subheader(entity.get('name', 'No Name'))
            st.write("Description:", entity.get('description', 'No Description'))
            if 'detailedDescription' in entity:
                detailed_desc = entity['detailedDescription']
                st.write("Detailed Description:", detailed_desc.get('articleBody', 'No Detailed Description'))
                st.write("Source:", detailed_desc.get('url', 'No URL'))
            if 'image' in entity:
                st.image(entity['image']['contentUrl'], caption='Image of ' + entity['name'])
            st.write("Type(s):", ', '.join(entity.get('@type', 'No Type')))
            st.write("Result Score:", element.get('resultScore', 'No Score'))
            st.markdown("---")
    else:
        st.write("No results found.")
