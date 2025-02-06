import streamlit as st
from handlear import download_file, get_files, generate_images

desired_size = (600, 400)

st.title("🖼️ Image Generation Gallery ✨")
margin = '<div style="margin: 20px 5px;"></div>'

# User input form
with st.form("user_form", clear_on_submit=True):
    user_input = st.text_input("Type Something")
    submit_button = st.form_submit_button(label="Send")

if submit_button:
    try:
        with st.spinner("Generating Image..."):
            image_url = generate_images(user_input)
            st.image(image_url, caption="Generated Image")
            message = download_file(user_input, image_url)
            st.success(message)
    except Exception as e:
        st.error(f"An error occurred: {e}")


def display_gallery():
    """Display images in the gallery"""
    images = get_files()
    length = len(images)
    st.markdown(margin, unsafe_allow_html=True)

    for i in range(0, length, 2):
        col1, col2 = st.columns(2)

        with col1:
            if i < length:
                image_resized = images[i]["file"].resize(desired_size)
                st.image(image_resized, caption=images[i]["title"])

        with col2:
            if i + 1 < length:
                image_resized = images[i + 1]["file"].resize(desired_size)
                st.image(image_resized, caption=images[i + 1]["title"])


if __name__ == "__main__":
    display_gallery()
