import streamlit as st
import pickle
import numpy as np

# Load semua model dan data
popular_df = pickle.load(open('popular.pkl', 'rb'))
dfbooks = pickle.load(open('dfbooks.pkl', 'rb'))
xdf_pivot = pickle.load(open('xdf_pivot.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

# Setup halaman
st.set_page_config(page_title="Book Recommender", layout="wide")
st.title("📚 My Book Recommender System")

# Navigasi menu
menu = st.sidebar.radio("Menu", ["Home", "Recommender", "Contact"])

# Home Page: Tampilkan Buku Populer
if menu == "Home":
    st.subheader("🔥 Popular Books")

    for i in range(0, len(popular_df), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(popular_df):
                with cols[j]:
                    st.image(popular_df['Image-URL-M'].iloc[i + j], width=120)
                    st.write(f"**{popular_df['Book-Title'].iloc[i + j]}**")
                    st.caption(f"by {popular_df['Book-Author'].iloc[i + j]}")
                    st.markdown(f"⭐ {popular_df['avg_rating'].iloc[i + j]} ({popular_df['num_ratings'].iloc[i + j]} ratings)")

# Recommender Page
elif menu == "Recommender":
    st.subheader("🔍 Get Book Recommendations")
    with st.form("recommendation_form"):
        user_input = st.text_input("Buku apa yang sudah kamu baca? :")
        submitted = st.form_submit_button("Recommend")

    if submitted and user_input:
        try:
            indx = np.where(xdf_pivot.index == user_input)[0][0]
            similar_books = sorted(list(enumerate(similarity_score[indx])), key=lambda x: x[1], reverse=True)[1:11]

            st.write(f"### 📘 Rekomendasi Buku yang serupa **{user_input}**:")
            cols = st.columns(5)
            for idx, book in enumerate(similar_books):
                temp_df = dfbooks[dfbooks['Book-Title'] == xdf_pivot.index[book[0]]]
                title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
                author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
                image = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

                with cols[idx % 5]:
                    st.image(image, width=120)
                    st.write(f"**{title}**")
                    st.caption(f"by {author}")

        except IndexError:
            st.error("Book not found. Please check the title and try again.")

# Contact Page
elif menu == "Contact":
    st.subheader("📞 Contact Us")
    st.write("For inquiries or support, please email us at: asyecandra@gmail.com")
    st.write("You can also reach us on social media:")
    st.markdown("- Facebook: [@andygaluh]")
    st.markdown("- Instagram: [@itsme_gaca]")