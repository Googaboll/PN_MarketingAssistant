import openai
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configure OpenAI API key
# Configure OpenAI API key - try multiple approaches to handle different secret formats
try:
    openai.api_key = st.secrets["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"]
except:
    try:
        openai.api_key = st.secrets.openai_api_key
    except:
        st.error("Error: Unable to access API key from secrets. Please check your configuration.")

# Configure the page
st.set_page_config(
    page_title="Positive News Marketing Copy Assistant",
    page_icon="📰",
    layout="wide"
)

# Title and description
st.title("Positive News Marketing Copy Assistant")
st.markdown("""
This tool helps transform product copy into marketing content for new issue promotion.
Simply enter the issue details and copy below, and the tool will generate pre-launch and launch marketing materials.
""")

# Issue information
st.header("Issue Information")
col1, col2, col3 = st.columns(3)
with col1:
    issue_number = st.text_input("Issue Number (e.g., 121)", "121")
with col2:
    publication_date = st.date_input("Publication Date", datetime.now() + timedelta(days=14))
with col3:
    season = st.selectbox("Season", ["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"])

# Get cover image
cover_image = st.file_uploader("Upload Cover Image (optional)", type=["jpg", "png", "jpeg"])

# Product copy
st.header("Product Copy")
product_copy = st.text_area("Paste Lucy's product copy here", height=250, 
                           placeholder="Example: Positive News #121, Apr-Jun 2025\nCover story: [Title] – [Subtitle]\n[Description]\n\nOther features include: [Feature 1] • [Feature 2] • [Feature 3]...")

# Special offers
st.header("Special Offer (Optional)")
has_offer = st.checkbox("Include special offer")
offer_details = ""
if has_offer:
    offer_details = st.text_area("Offer details", height=100, 
                              placeholder="Example: Save 20% on annual subscriptions with code SPRING25")

# Generate the content using OpenAI API
def generate_marketing_content(product_copy, issue_number, publication_date, season, offer_details, content_type):
    
    # Format dates
    pub_date_str = publication_date.strftime("%d %b")
    pre_launch_start = (publication_date - timedelta(days=7)).strftime("%d %b")
    
    # Create prompt for the specific content type
    if content_type == "pre_launch":
        prompt = f"""
        You are a marketing specialist for Positive News, a magazine that focuses on constructive, solution-focused journalism.
        
        Using the product copy below, create pre-launch marketing copy for issue #{issue_number} ({season} 2025) that will be published on {pub_date_str}.
        
        Pre-launch copy should include:
        1. Clear OBJECTIVE (promote new issue and drive subscription sales)
        2. USAGE PERIOD (from {pre_launch_start} to {(publication_date - timedelta(days=1)).strftime("%d %b")})
        3. Newsletter CTA content with button text and link
        4. Cover reveal social post copy for Facebook, Twitter/X
        5. 3-5 pre-launch general posts for social media (Facebook/Instagram with link instruction and Twitter versions)
        
        Product Copy:
        {product_copy}
        
        {'Include this special offer information: ' + offer_details if offer_details else 'No special offer for this issue.'}
        
        Use the tone and style from these examples:
        - "We're excited to reveal the front cover of the new issue of Positive News magazine."
        - "In 2025, choose to focus on what's going right, with Positive News magazine."
        - "Subscribe now to be among the first to get a copy"
        
        Format the output exactly like a marketing brief document with clear sections and social posts numbered.
        """
    elif content_type == "launch":
        prompt = f"""
        You are a marketing specialist for Positive News, a magazine that focuses on constructive, solution-focused journalism.
        
        Using the product copy below, create launch marketing copy for issue #{issue_number} ({season} 2025) that will be published on {pub_date_str}.
        
        Launch copy should include:
        1. Clear OBJECTIVE (promote new issue and drive subscription sales)
        2. USAGE PERIOD (from {pub_date_str} to {(publication_date + timedelta(days=20)).strftime("%d %b")})
        3. Newsletter CTA content for two weekends after launch
        4. 4-5 launch social posts for various platforms (Facebook/Instagram with link instruction and Twitter versions)
        
        Product Copy:
        {product_copy}
        
        {'Include this special offer information: ' + offer_details if offer_details else 'No special offer for this issue.'}
        
        Use the tone and style from these examples:
        - "The inspiring new issue of Positive News magazine is out now."
        - "From our cover story about X, to features on Y and Z – it's filled with uplifting, enquiring stories of hope and change."
        - "Subscribe now to get your copy"
        
        Format the output exactly like a marketing brief document with clear sections and social posts numbered.
        """
    elif content_type == "schedule":
        prompt = f"""
        You are a marketing specialist for Positive News, a magazine that focuses on constructive, solution-focused journalism.
        
        Create a detailed marketing schedule for issue #{issue_number} ({season} 2025) that will be published on {pub_date_str}.
        
        The schedule should cover from {pre_launch_start} to {(publication_date + timedelta(days=20)).strftime("%d %b")}, and include:
        
        1. Pre-launch phase (cover reveal and pre-order promotion)
        2. Launch phase (out now promotion)
        3. Specific posts for Facebook, Twitter/X, Instagram, and LinkedIn
        4. Newsletter promotions
        
        Format as a markdown table with columns for:
        - Date
        - Platform
        - Content Type (Cover Reveal, General Pre-launch, Launch, etc.)
        - Notes/Links
        
        The schedule should follow Positive News' pattern:
        - Cover reveal happens ~7 days before publication
        - Newsletter promotions on Saturdays
        - 1-2 social posts per day during pre-launch
        - Pinned "out now" post on publication day
        - Regular posts for 2-3 weeks after launch
        
        Make the schedule realistic and practical for a small team to implement.
        """
    
    # Call the OpenAI API
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful marketing assistant for Positive News magazine."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content

# Generate buttons
st.header("Generate Marketing Content")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Generate Pre-Launch Copy", type="primary"):
        if product_copy:
            with st.spinner("Generating pre-launch marketing copy..."):
                pre_launch_copy = generate_marketing_content(
                    product_copy, 
                    issue_number, 
                    publication_date, 
                    season, 
                    offer_details,
                    "pre_launch"
                )
                st.session_state.pre_launch_copy = pre_launch_copy
        else:
            st.error("Please enter product copy first.")

with col2:
    if st.button("Generate Launch Copy", type="primary"):
        if product_copy:
            with st.spinner("Generating launch marketing copy..."):
                launch_copy = generate_marketing_content(
                    product_copy, 
                    issue_number, 
                    publication_date, 
                    season, 
                    offer_details,
                    "launch"
                )
                st.session_state.launch_copy = launch_copy
        else:
            st.error("Please enter product copy first.")

with col3:
    if st.button("Generate Marketing Schedule", type="primary"):
        if product_copy:
            with st.spinner("Generating marketing schedule..."):
                schedule = generate_marketing_content(
                    product_copy, 
                    issue_number, 
                    publication_date, 
                    season, 
                    offer_details,
                    "schedule"
                )
                st.session_state.schedule = schedule
        else:
            st.error("Please enter product copy first.")

# Display generated content
tabs = st.tabs(["Pre-Launch Copy", "Launch Copy", "Marketing Schedule"])

with tabs[0]:
    if "pre_launch_copy" in st.session_state:
        st.markdown("### Pre-Launch Marketing Copy")
        st.text_area("Copy this content", st.session_state.pre_launch_copy, height=400)
        st.download_button(
            label="Download Pre-Launch Copy",
            data=st.session_state.pre_launch_copy,
            file_name=f"positive_news_{issue_number}_pre_launch_copy.txt",
            mime="text/plain"
        )

with tabs[1]:
    if "launch_copy" in st.session_state:
        st.markdown("### Launch Marketing Copy")
        st.text_area("Copy this content", st.session_state.launch_copy, height=400)
        st.download_button(
            label="Download Launch Copy",
            data=st.session_state.launch_copy,
            file_name=f"positive_news_{issue_number}_launch_copy.txt",
            mime="text/plain"
        )

with tabs[2]:
    if "schedule" in st.session_state:
        st.markdown("### Marketing Schedule")
        st.markdown(st.session_state.schedule)
        st.download_button(
            label="Download Marketing Schedule",
            data=st.session_state.schedule,
            file_name=f"positive_news_{issue_number}_marketing_schedule.md",
            mime="text/plain"
        )
