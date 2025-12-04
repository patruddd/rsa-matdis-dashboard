import streamlit as st
import random

def is_prime(n, k=5):
    """
    Miller-Rabin primality test.
    Returns True if n is probably prime, False otherwise.
    """
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^s * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Repeat k times
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """
    Generates a probable prime number of the given bit length.
    """
    while True:
        p = random.getrandbits(bits)
        # Ensure the number is odd and within the bit length range
        p |= (1 << bits - 1) | 1 # Set MSB and LSB to 1
        if is_prime(p):
            return p

def gcd(a, b):
    """
    Calculates the Greatest Common Divisor (GCD) of a and b using Euclidean algorithm.
    """
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """
    Calculates the modular multiplicative inverse of a modulo m using Extended Euclidean Algorithm.
    Returns x such that (a * x) % m == 1.
    """
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x

def generate_keypair(bits=1024):
    """
    Generates an RSA public and private key pair.
    Returns ((n, e), (n, d)).
    """
    st.info(f"Step 1: Generating two large prime numbers (p and q) of {bits // 2} bits each...")

    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Tampilkan p dan q tanpa backtick agar tidak "kotak-kotak"
    st.success("Generated Prime Numbers:")
    st.code(f"p = {p}\nq = {q}", language="text")

    # Expander untuk melihat nilai lengkap (lebih rapi)
    with st.expander("View Prime Numbers (p and q)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Prime p:**")
            st.code(str(p), language="text")
        with col2:
            st.markdown("**Prime q:**")
            st.code(str(q), language="text")

    st.info(f"Step 2: Calculate n = p × q =\n{n}")
    st.info(f"Step 3: Calculate Euler's totient φ(n) = (p-1)×(q-1) =\n{phi}")

    # Pilih e
    st.info("Step 4: Choose public exponent (e) such that 1 < e < φ(n) and gcd(e, φ(n)) = 1")
    e = 65537  # Lebih cepat dan aman (umum digunakan)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    st.info("Step 5: Calculate private exponent (d) as the modular multiplicative inverse of e modulo φ(n)")
    d = mod_inverse(e, phi)

    # Tampilkan e dan d tanpa backtick juga
    st.success(f"Key Parameters Generated:\nPublic exponent (e) = {e}\nPrivate exponent (d) = {d}")

    with st.expander("View Full Key Parameters", expanded=False):
        st.markdown("**Public exponent (e):**")
        st.code(str(e), language="text")
        st.markdown("**Private exponent (d):**")
        st.code(str(d), language="text")
        st.markdown("**Modulus (n):**")
        st.code(str(n), language="text")

    return ((n, e), (n, d))

def encrypt(public_key, plaintext):
    """
    Encrypts the plaintext using the public key.
    Converts string to integers, encrypts each, returns list of integers.
    Note: This is a simplified character-by-character encryption for demonstration.
          In real RSA, entire messages/blocks are converted to numbers and padded.
    """
    n, e = public_key

    encrypted_msg_chars = []

    for char in plaintext:
        char_as_int = ord(char)
        # Check if character's ASCII value is too large for the key's 'n' value
        # This check is mostly for conceptual understanding in this simple demo,
        # as 'n' will usually be much larger than any char value in real RSA.
        if char_as_int >= n:
            st.error(f"❌ **Error:** Character '{char}' (ASCII: {char_as_int}) is too large for the current key (n={n})."
                     " This simplified demo requires `ord(char) < n`. Please consider a larger key size"
                     " or a simpler message (e.g., ASCII characters).")
            return [] # Indicate error

        encrypted_char = pow(char_as_int, e, n)
        encrypted_msg_chars.append(encrypted_char)

    return encrypted_msg_chars

def decrypt(private_key, ciphertext):
    """
    Decrypts the ciphertext using the private key.
    Converts list of integers back to string.
    """
    n, d = private_key

    decrypted_chars = []
    for char_code in ciphertext:
        decrypted_char_int = pow(char_code, d, n)
        decrypted_chars.append(chr(decrypted_char_int))

    return "".join(decrypted_chars)

# --- Custom CSS for Professional Styling ---
def load_custom_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --danger-color: #d62728;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    
    .info-card h4 {
        color: #2c3e50;
    }
    
    .key-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 2px solid #e0e0e0;
        transition: transform 0.2s;
        color: #2c3e50;
    }
    
    .key-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    /* Section headers */
    .section-header {
        color: #667eea;
        font-weight: 700;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Metric styling */
    .metric-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        min-width: 150px;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Step indicators */
    .step-indicator {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        margin-right: 0.5rem;
        font-size: 0.9rem;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    /* Fix long text overflow in code blocks */
    .stCodeBlock code {
        word-wrap: break-word;
        white-space: pre-wrap;
        overflow-wrap: break-word;
    }
    
    /* Alternative: Add horizontal scroll if preferred */
    pre {
        overflow-x: auto;
        white-space: pre;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Warning and info boxes */
    .warning-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #856404;
    }
    
    .warning-box h3, .warning-box h4 {
        color: #856404;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #155724;
    }
    
    .success-box h3, .success-box h4 {
        color: #155724;
    }
    
    .success-box p {
        color: #155724;
    }
    
    /* Progress bar custom styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f0f2f6;
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Streamlit Application ---

st.set_page_config(
    page_title="RSA Cryptography Suite",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Main header
st.markdown("""
<div class="main-header">
    <h1>🔐 RSA Cryptography Suite</h1>
    <p>Professional Educational Platform for RSA Encryption & Decryption</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for keys and messages
if 'public_key' not in st.session_state:
    st.session_state.public_key = None
if 'private_key' not in st.session_state:
    st.session_state.private_key = None
if 'encrypted_msg' not in st.session_state:
    st.session_state.encrypted_msg = []
if 'original_msg' not in st.session_state:
    st.session_state.original_msg = ""
if 'decrypted_msg' not in st.session_state:
    st.session_state.decrypted_msg = ""

# Sidebar navigation with enhanced styling
st.sidebar.markdown("### 🧭 Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Select a section:",
    ["🔑 Key Generation", "🔒 Encryption", "🔓 Decryption & Verification"],
    label_visibility="collapsed"
)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 About RSA")
st.sidebar.info(
    "**RSA** (Rivest-Shamir-Adleman) is one of the first public-key cryptosystems "
    "and is widely used for secure data transmission. It relies on the practical "
    "difficulty of factoring the product of two large prime numbers."
)

st.sidebar.markdown("### 🎯 Key Concepts")
with st.sidebar.expander("📖 Learn More"):
    st.markdown("""
    **Public Key Cryptography:**
    - Uses a pair of keys (public & private)
    - Public key encrypts, private key decrypts
    - Ensures secure communication
    
    **RSA Algorithm Steps:**
    1. Generate two large primes (p, q)
    2. Calculate n = p × q
    3. Calculate φ(n) = (p-1)(q-1)
    4. Choose public exponent e
    5. Calculate private exponent d
    """)

# --- Section 1: Key Generation ---
if page == "🔑 Key Generation":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">🔑 RSA Key Pair Generation</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
        Generate a pair of cryptographic keys for RSA encryption and decryption. 
        The security of RSA depends on the key size - larger keys are more secure but take longer to generate.
        </div>
        """, unsafe_allow_html=True)
    
    # Key size selection
    st.markdown("#### ⚙️ Configuration")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        key_bits = st.select_slider(
            "Select Key Size (bits)",
            options=[128, 256, 384, 512, 768, 1024, 1536, 2048],
            value=512,
            help="Larger key sizes provide better security but take longer to generate"
        )
    
    with col2:
        st.metric("Prime Bits", f"{key_bits // 2}", help="Each prime number size")
    
    with col3:
        security_level = "Low" if key_bits < 512 else "Medium" if key_bits < 1024 else "High"
        st.metric("Security", security_level)
    
    st.info(f"📊 This will generate two prime numbers of **{key_bits // 2} bits** each, "
            f"resulting in a modulus (n) of approximately **{key_bits} bits**.")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate RSA Key Pair", type="primary", use_container_width=True):
            with st.spinner("🔄 Generating cryptographic keys..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                
                public, private = generate_keypair(key_bits)
                st.session_state.public_key = public
                st.session_state.private_key = private
                
                st.balloons()
                st.success("✅ Keys generated successfully!")
    
    # Display generated keys
    if st.session_state.public_key and st.session_state.private_key:
        st.markdown("---")
        st.markdown('<h3 class="section-header">🔑 Generated Key Pair</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🌐 Public Key (Share Freely)")
            st.markdown("""
            <div class="key-card">
            Use this key to <strong>encrypt</strong> messages. It's safe to share publicly.
            </div>
            """, unsafe_allow_html=True)
            
            n_pub, e_pub = st.session_state.public_key
            
            with st.expander("📋 View Public Key Details", expanded=True):
                st.markdown("**Modulus (n):**")
                st.text_area("n", str(n_pub), height=100, label_visibility="collapsed", key="pub_n")
                st.markdown("**Public Exponent (e):**")
                st.text_area("e", str(e_pub), height=60, label_visibility="collapsed", key="pub_e")
            
            st.metric("Modulus Length", f"{len(str(n_pub))} digits")
        
        with col2:
            st.markdown("##### 🔒 Private Key (Keep Secret)")
            st.markdown("""
            <div class="key-card" style="border-color: #d62728;">
            Use this key to <strong>decrypt</strong> messages. Never share this key!
            </div>
            """, unsafe_allow_html=True)
            
            n_priv, d_priv = st.session_state.private_key
            
            with st.expander("📋 View Private Key Details", expanded=True):
                st.markdown("**Modulus (n):**")
                st.text_area("n", str(n_priv), height=100, label_visibility="collapsed", key="priv_n")
                st.markdown("**Private Exponent (d):**")
                st.text_area("d", str(d_priv), height=100, label_visibility="collapsed", key="priv_d")
            
            st.warning("🚨 **Security Warning:** Keep your private key confidential at all times!")

# --- Section 2: Encryption ---
elif page == "🔒 Encryption":
    st.markdown('<h2 class="section-header">🔒 Message Encryption</h2>', unsafe_allow_html=True)
    
    if st.session_state.public_key:
        n_pub, e_pub = st.session_state.public_key
        
        # Display current key info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-box">
                <div class="metric-label">Public Modulus (n)</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(str(n_pub)[:20] + "..."), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-box">
                <div class="metric-label">Public Exponent (e)</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(e_pub), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-box">
                <div class="metric-label">Key Size</div>
                <div class="metric-value">{} bits</div>
            </div>
            """.format(len(bin(n_pub)) - 2), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Message input
        st.markdown("#### 📝 Enter Your Message")
        message_to_encrypt = st.text_area(
            "Plaintext Message",
            st.session_state.original_msg if st.session_state.original_msg else "Halo, ini adalah pesan rahasia dari Matematika Diskrit!",
            height=120,
            help="Enter the message you want to encrypt"
        )
        st.session_state.original_msg = message_to_encrypt
        
        # Character count
        char_count = len(message_to_encrypt)
        st.caption(f"📊 Character count: **{char_count}** characters")
        
        # Encrypt button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔐 Encrypt Message", type="primary", use_container_width=True):
                if not st.session_state.public_key:
                    st.error("🚫 Please generate keys in the 'Key Generation' section first.")
                else:
                    with st.spinner("🔄 Encrypting your message..."):
                        encrypted_data = encrypt(st.session_state.public_key, message_to_encrypt)
                        if encrypted_data:
                            st.session_state.encrypted_msg = encrypted_data
                            st.success("✅ Message encrypted successfully!")
                            
                            st.markdown("---")
                            st.markdown("#### 🔐 Encrypted Output")
                            
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.code(str(st.session_state.encrypted_msg), language="python")
                            with col2:
                                st.metric("Encrypted Blocks", len(encrypted_data))
                            
                            st.info("💡 Each number represents an encrypted character. "
                                   "This ciphertext can only be decrypted with the corresponding private key.")
                            
                            with st.expander("🔍 View Encryption Details"):
                                st.markdown("**Original Message:**")
                                st.text(message_to_encrypt)
                                st.markdown("**Encrypted Values (first 5):**")
                                for i, val in enumerate(encrypted_data[:5]):
                                    char = message_to_encrypt[i]
                                    st.text(f"'{char}' (ASCII {ord(char)}) → {val}")
                        else:
                            st.error("❌ Encryption failed. Please check the error message above.")
    else:
        st.markdown("""
        <div class="info-card">
        <h4>⚠️ No Keys Available</h4>
        <p>Please generate RSA keys in the <strong>Key Generation</strong> section first before encrypting messages.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔑 Go to Key Generation"):
            st.session_state.page = "🔑 Key Generation"
            st.rerun()

# --- Section 3: Decryption & Verification ---
elif page == "🔓 Decryption & Verification":
    st.markdown('<h2 class="section-header">🔓 Message Decryption & Verification</h2>', unsafe_allow_html=True)
    
    if st.session_state.private_key:
        n_priv, d_priv = st.session_state.private_key
        
        # Display current key info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-box" style="background: linear-gradient(135deg, #d62728 0%, #ff7f0e 100%);">
                <div class="metric-label">Private Modulus (n)</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(str(n_priv)[:20] + "..."), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-box" style="background: linear-gradient(135deg, #d62728 0%, #ff7f0e 100%);">
                <div class="metric-label">Private Exponent (d)</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(str(d_priv)[:20] + "..."), unsafe_allow_html=True)
        
        with col3:
            encrypted_count = len(st.session_state.encrypted_msg) if st.session_state.encrypted_msg else 0
            st.markdown("""
            <div class="metric-box" style="background: linear-gradient(135deg, #d62728 0%, #ff7f0e 100%);">
                <div class="metric-label">Encrypted Blocks</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(encrypted_count), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display encrypted message
        st.markdown("#### 🔐 Encrypted Message to Decrypt")
        
        # Add option to use existing encrypted message or input manual
        decrypt_option = st.radio(
            "Choose decryption method:",
            ["Use Last Encrypted Message", "Input Ciphertext Manually"],
            horizontal=True
        )
        
        if decrypt_option == "Use Last Encrypted Message":
            if st.session_state.encrypted_msg:
                with st.expander("📋 View Encrypted Data", expanded=True):
                    st.code(str(st.session_state.encrypted_msg), language="python")
                ciphertext_to_decrypt = st.session_state.encrypted_msg
            else:
                st.warning("⚠️ No encrypted message available. Please encrypt a message first or use manual input.")
                ciphertext_to_decrypt = []
        else:
            st.markdown("**Enter Ciphertext (Python list format):**")
            manual_cipher = st.text_area(
                "Ciphertext",
                placeholder="[12345, 67890, 11121, ...]",
                height=100,
                help="Enter the encrypted message as a Python list of integers"
            )
            try:
                if manual_cipher.strip():
                    ciphertext_to_decrypt = eval(manual_cipher)
                    st.success(f"✓ Valid ciphertext with {len(ciphertext_to_decrypt)} encrypted blocks")
                else:
                    ciphertext_to_decrypt = []
            except:
                st.error("❌ Invalid format. Please enter a valid Python list of integers.")
                ciphertext_to_decrypt = []
        
        # Decrypt button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔓 Decrypt Message", type="primary", use_container_width=True):
                if not st.session_state.private_key:
                    st.error("🚫 Please generate keys first.")
                elif not ciphertext_to_decrypt:
                    st.error("🚫 No message to decrypt. Please encrypt a message first or input ciphertext manually.")
                else:
                    with st.spinner("🔄 Decrypting your message..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            progress_bar.progress(i + 1)
                        
                        decrypted_message = decrypt(st.session_state.private_key, ciphertext_to_decrypt)
                        st.session_state.decrypted_msg = decrypted_message
                        st.success("✅ Message decrypted successfully!")
                        
                        st.markdown("---")
                        st.markdown("#### 📜 Decrypted Message")
                        st.markdown("""
                        <div class="success-box">
                        <h4>Decrypted Plaintext:</h4>
                        <p style="font-size: 1.1rem; font-weight: 500;">{}</p>
                        </div>
                        """.format(decrypted_message), unsafe_allow_html=True)
                        
                        # Verification section
                        st.markdown("---")
                        st.markdown("#### ✅ Verification Process")
                        
                        if st.session_state.original_msg == st.session_state.decrypted_msg:
                            st.markdown("""
                            <div class="success-box">
                            <h3>🎉 Verification Successful!</h3>
                            <p><strong>Result:</strong> The decrypted message matches the original message perfectly.</p>
                            <p><strong>Status:</strong> ✓ Encryption and decryption process completed successfully.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Original Length", f"{len(st.session_state.original_msg)} chars", delta="Match")
                            with col2:
                                st.metric("Decrypted Length", f"{len(st.session_state.decrypted_msg)} chars", delta="Match")
                            
                        else:
                            st.markdown("""
                            <div class="warning-box">
                            <h3>❌ Verification Failed!</h3>
                            <p><strong>Result:</strong> The decrypted message does NOT match the original message.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Original Message:**")
                                st.code(st.session_state.original_msg)
                            with col2:
                                st.markdown("**Decrypted Message:**")
                                st.code(st.session_state.decrypted_msg)
                        
                        # Detailed comparison
                        with st.expander("🔍 View Detailed Comparison"):
                            st.markdown("**Character-by-Character Comparison:**")
                            comparison_df_data = []
                            for i in range(min(len(st.session_state.original_msg), len(st.session_state.decrypted_msg))):
                                orig_char = st.session_state.original_msg[i]
                                dec_char = st.session_state.decrypted_msg[i]
                                match = "✓" if orig_char == dec_char else "✗"
                                comparison_df_data.append({
                                    "Position": i + 1,
                                    "Original": orig_char,
                                    "Decrypted": dec_char,
                                    "Match": match
                                })
                            
                            if comparison_df_data:
                                st.dataframe(comparison_df_data[:20], use_container_width=True)
                                if len(comparison_df_data) > 20:
                                    st.caption(f"Showing first 20 of {len(comparison_df_data)} characters")
    else:
        st.markdown("""
        <div class="info-card">
        <h4>⚠️ Prerequisites Required</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.private_key:
            st.warning("🔑 Please generate RSA keys in the **Key Generation** section.")
        
        if st.session_state.private_key and not st.session_state.encrypted_msg:
            st.info("💡 Once you encrypt a message, it will automatically appear here for decryption, or you can input ciphertext manually.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f0f2f6; border-radius: 10px; margin-top: 3rem;">
    <h4>📚 Educational Notice</h4>
    <p style="color: #666;">
    This is a <strong>simplified RSA implementation</strong> for educational purposes. 
    Real-world RSA implementations use more complex padding schemes (e.g., OAEP) 
    and typically encrypt symmetric keys (which then encrypt the message) rather than raw messages directly.
    </p>
    <p style="color: #666; margin-top: 1rem;">
    Character-by-character encryption as demonstrated here is inefficient and has security limitations.
    </p>
    <p style="margin-top: 1.5rem; color: #888; font-size: 0.9rem;">
    🔐 Built with Streamlit | RSA Cryptography Educational Suite
    </p>
</div>
""", unsafe_allow_html=True)