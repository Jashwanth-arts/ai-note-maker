   import base64
   import streamlit as st
   import anthropic
   from fpdf import FPDF

   st.set_page_config(page_title="AI Note Maker", page_icon="📝")
   st.title("📝 AI Note Maker")
   st.write("Upload a photo of your notebook page and get clean notes in 30 seconds.")

   lang = st.selectbox("Language", ["English", "Hindi", "English + Hindi"])
   file = st.file_uploader("Upload notebook photo", type=["jpg", "jpeg", "png"])


   def make_notes(img_bytes, media_type, lang):
       client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
       data = base64.b64encode(img_bytes).decode()
       prompt = (
           "Read the handwriting in this image. Fix spelling mistakes. "
           "Make clean study notes with a heading, bullet points (start each "
           "with '- ') and a short summary at the end. "
           f"Write the notes in: {lang}. Do not use markdown symbols like # or **."
       )
       reply = client.messages.create(
           model="claude-haiku-5-5",
           max_tokens=1500,
           messages=[{
               "role": "user",
               "content": [
                   {"type": "image", "source": {
                       "type": "base64", "media_type": media_type, "data": data}},
                   {"type": "text", "text": prompt},
               ],
           }],
       )
       return reply.content[0].text


   def make_pdf(text):
       pdf = FPDF()
       pdf.add_page()
       pdf.add_font("Noto", "", "NotoSansDevanagari-Regular.ttf")
       pdf.set_font("Noto", size=12)
       pdf.set_text_shaping(True)
       pdf.multi_cell(0, 8, text)
       return bytes(pdf.output())


   if file and st.button("Make Notes ✨"):
       with st.spinner("Reading your handwriting..."):
           notes = make_notes(file.getvalue(), file.type, lang)
       st.subheader("Your Clean Notes")
       st.write(notes)
       st.download_button("⬇️ Download PDF", make_pdf(notes),
                          file_name="my_notes.pdf", mime="application/pdf")
