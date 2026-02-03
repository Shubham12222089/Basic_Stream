import streamlit as st

st.set_page_config(page_title="Valentine 💖", layout="wide")

# Hide default Streamlit UI elements
st.markdown(
    """
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {background: transparent;}
    </style>
    """,
    unsafe_allow_html=True
)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@400;600;800&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: 'Poppins', sans-serif;
        }

        /* Animated Gradient Background */
        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(-45deg, #ff6b9d, #ff8e72, #ff6b9d, #c44569);
            background-size: 400% 400%;
            animation: gradientShift 8s ease infinite;
            z-index: -2;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Particle Container */
        #particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        /* Floating Hearts */
        .heart {
            position: absolute;
            color: rgba(255, 255, 255, 0.6);
            animation: floatUp linear infinite;
            pointer-events: none;
            text-shadow: 0 0 10px rgba(255, 100, 150, 0.5);
        }

        @keyframes floatUp {
            0% {
                transform: translateY(100vh) rotate(0deg) scale(0.5);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-20vh) rotate(360deg) scale(1.2);
                opacity: 0;
            }
        }

        /* Sparkle Effect */
        .sparkle {
            position: absolute;
            width: 6px;
            height: 6px;
            background: white;
            border-radius: 50%;
            animation: sparkle 2s ease-in-out infinite;
            box-shadow: 0 0 10px white, 0 0 20px #ff6b9d;
        }

        @keyframes sparkle {
            0%, 100% { opacity: 0; transform: scale(0); }
            50% { opacity: 1; transform: scale(1); }
        }

        /* Main Container */
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        /* Card Design */
        .card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 40px;
            padding: 60px 80px;
            text-align: center;
            box-shadow: 
                0 25px 60px rgba(0, 0, 0, 0.2),
                inset 0 0 60px rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            max-width: 600px;
            width: 100%;
            animation: cardFloat 4s ease-in-out infinite;
            position: relative;
            overflow: visible;
        }

        @keyframes cardFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        /* Decorative Heart Icons */
        .card::before,
        .card::after {
            content: '💕';
            position: absolute;
            font-size: 40px;
            animation: bounce 2s ease-in-out infinite;
        }

        .card::before {
            top: -25px;
            left: 30px;
        }

        .card::after {
            top: -25px;
            right: 30px;
            animation-delay: 0.5s;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        /* Title Styling */
        .title {
            font-family: 'Dancing Script', cursive;
            font-size: 56px;
            font-weight: 700;
            color: #fff;
            text-shadow: 
                0 4px 15px rgba(0, 0, 0, 0.2),
                0 0 30px rgba(255, 100, 150, 0.5);
            margin-bottom: 15px;
            animation: titlePulse 2.5s ease-in-out infinite;
        }

        @keyframes titlePulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.03); }
        }

        /* Subtitle */
        .subtitle {
            font-size: 20px;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 40px;
            letter-spacing: 2px;
        }

        /* Heart Icon Animation */
        .heart-icon {
            font-size: 80px;
            display: inline-block;
            animation: heartbeat 1.2s ease-in-out infinite;
            margin-bottom: 30px;
            filter: drop-shadow(0 0 20px rgba(255, 100, 150, 0.8));
        }

        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            15% { transform: scale(1.15); }
            30% { transform: scale(1); }
            45% { transform: scale(1.1); }
            60% { transform: scale(1); }
        }

        /* Button Container */
        .btn-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 25px;
            flex-wrap: wrap;
            position: relative;
            min-height: 80px;
        }

        /* Button Base Styles */
        .btn {
            font-family: 'Poppins', sans-serif;
            font-size: 20px;
            font-weight: 600;
            padding: 16px 45px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }

        /* Yes Button */
        #yes-btn {
            background: linear-gradient(135deg, #ff2d55, #ff6b9d);
            color: white;
            box-shadow: 
                0 8px 25px rgba(255, 45, 85, 0.5),
                0 0 0 0 rgba(255, 45, 85, 0.4);
            animation: yesGlow 2s ease-in-out infinite;
        }

        @keyframes yesGlow {
            0%, 100% { box-shadow: 0 8px 25px rgba(255, 45, 85, 0.5), 0 0 0 0 rgba(255, 45, 85, 0.4); }
            50% { box-shadow: 0 8px 35px rgba(255, 45, 85, 0.7), 0 0 0 15px rgba(255, 45, 85, 0); }
        }

        #yes-btn:hover {
            transform: scale(1.15) translateY(-3px);
            box-shadow: 0 15px 40px rgba(255, 45, 85, 0.6);
        }

        #yes-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        /* No Button */
        #no-btn {
            background: linear-gradient(135deg, #e0e5ec, #c9d1d9);
            color: #555;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }

        #no-btn:hover {
            transform: scale(0.95);
        }

        /* ====== CELEBRATION SCREEN ====== */
        .celebration {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(-45deg, #ff2d55, #ff6b9d, #ff8e72, #c44569);
            background-size: 400% 400%;
            animation: gradientShift 5s ease infinite;
            text-align: center;
            padding: 20px;
            z-index: 1000;
        }

        .celebration-content {
            animation: celebrateIn 1s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }

        @keyframes celebrateIn {
            0% { transform: scale(0) rotate(-10deg); opacity: 0; }
            100% { transform: scale(1) rotate(0deg); opacity: 1; }
        }

        .celebration h1 {
            font-family: 'Dancing Script', cursive;
            font-size: 80px;
            color: white;
            text-shadow: 0 5px 25px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
            animation: celebrateText 0.8s ease-out 0.3s both;
        }

        @keyframes celebrateText {
            0% { transform: translateY(50px); opacity: 0; }
            100% { transform: translateY(0); opacity: 1; }
        }

        .celebration h2 {
            font-size: 36px;
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: 25px;
            animation: celebrateText 0.8s ease-out 0.5s both;
        }

        .celebration .emoji-row {
            font-size: 60px;
            margin: 30px 0;
            animation: emojiPop 0.8s ease-out 0.7s both;
        }

        @keyframes emojiPop {
            0% { transform: scale(0); }
            70% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }

        .celebration p {
            font-size: 22px;
            color: rgba(255, 255, 255, 0.9);
            max-width: 500px;
            animation: celebrateText 0.8s ease-out 0.9s both;
        }

        /* Dancing Emojis */
        .dancers-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
            animation: celebrateText 0.8s ease-out 1.1s both;
        }

        .dancer {
            font-size: 70px;
            display: inline-block;
            animation: dance 0.5s ease-in-out infinite alternate;
        }

        .dancer:nth-child(1) { animation-delay: 0s; }
        .dancer:nth-child(2) { animation-delay: 0.1s; }
        .dancer:nth-child(3) { animation-delay: 0.2s; }
        .dancer:nth-child(4) { animation-delay: 0.3s; }
        .dancer:nth-child(5) { animation-delay: 0.4s; }

        @keyframes dance {
            0% {
                transform: translateY(0) rotate(-15deg) scale(1);
            }
            50% {
                transform: translateY(-20px) rotate(0deg) scale(1.1);
            }
            100% {
                transform: translateY(0) rotate(15deg) scale(1);
            }
        }

        .dancer-wrapper {
            animation: sway 1s ease-in-out infinite;
        }

        .dancer-wrapper:nth-child(even) {
            animation-direction: reverse;
        }

        @keyframes sway {
            0%, 100% { transform: translateX(-10px); }
            50% { transform: translateX(10px); }
        }

        /* Floating dancers on sides */
        .side-dancer {
            position: fixed;
            font-size: 80px;
            animation: sideDance 1s ease-in-out infinite;
            z-index: 1002;
        }

        .side-dancer.left {
            left: 5%;
            top: 50%;
            transform: translateY(-50%);
        }

        .side-dancer.right {
            right: 5%;
            top: 50%;
            transform: translateY(-50%) scaleX(-1);
            animation-delay: 0.5s;
        }

        @keyframes sideDance {
            0%, 100% {
                transform: translateY(-50%) rotate(-10deg);
            }
            25% {
                transform: translateY(-60%) rotate(5deg);
            }
            50% {
                transform: translateY(-50%) rotate(10deg);
            }
            75% {
                transform: translateY(-40%) rotate(-5deg);
            }
        }

        /* Confetti */
        .confetti {
            position: fixed;
            width: 12px;
            height: 12px;
            animation: confettiFall linear forwards;
            z-index: 1001;
        }

        @keyframes confettiFall {
            0% {
                transform: translateY(-100vh) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh) rotate(720deg);
                opacity: 0;
            }
        }

        /* Responsive Design */
        @media (max-width: 600px) {
            .card {
                padding: 40px 30px;
                border-radius: 30px;
            }
            
            .title {
                font-size: 38px;
            }
            
            .subtitle {
                font-size: 16px;
            }
            
            .heart-icon {
                font-size: 60px;
            }
            
            .btn {
                font-size: 16px;
                padding: 14px 35px;
            }
            
            .celebration h1 {
                font-size: 50px;
            }
            
            .celebration h2 {
                font-size: 26px;
            }
            
            .celebration .emoji-row {
                font-size: 45px;
            }
            
            .dancer {
                font-size: 45px;
            }
            
            .dancers-container {
                gap: 10px;
                margin: 20px 0;
            }
            
            .side-dancer {
                font-size: 50px;
            }
            
            .side-dancer.left {
                left: 2%;
            }
            
            .side-dancer.right {
                right: 2%;
            }
        }
    </style>
</head>
<body>
    <div class="background"></div>
    <div id="particles"></div>

    <div class="container" id="main-container">
        <div class="card" id="card">
            <div class="heart-icon">💘</div>
            <div class="title">Will you be my Valentine?</div>
            <p class="subtitle">Make this day special ✨</p>
            <div class="btn-container">
                <button class="btn" id="yes-btn" onclick="handleYes()">YES 💖</button>
                <button class="btn" id="no-btn" onmouseover="handleNoHover()" onclick="handleNoHover()">NO 😜</button>
            </div>
        </div>
    </div>

    <script>
        // Generate floating hearts
        function createHeart() {
            const heart = document.createElement('div');
            heart.className = 'heart';
            const hearts = ['❤️', '💕', '💗', '💖', '💝', '🌹'];
            heart.innerHTML = hearts[Math.floor(Math.random() * hearts.length)];
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.fontSize = (Math.random() * 25 + 15) + 'px';
            heart.style.animationDuration = (Math.random() * 6 + 6) + 's';
            heart.style.animationDelay = Math.random() * 2 + 's';
            document.getElementById('particles').appendChild(heart);
            
            setTimeout(() => heart.remove(), 14000);
        }

        // Generate sparkles
        function createSparkle() {
            const sparkle = document.createElement('div');
            sparkle.className = 'sparkle';
            sparkle.style.left = Math.random() * 100 + 'vw';
            sparkle.style.top = Math.random() * 100 + 'vh';
            sparkle.style.animationDelay = Math.random() * 2 + 's';
            document.getElementById('particles').appendChild(sparkle);
            
            setTimeout(() => sparkle.remove(), 4000);
        }

        // Initialize particles
        for (let i = 0; i < 20; i++) {
            setTimeout(() => createHeart(), i * 300);
        }
        
        for (let i = 0; i < 15; i++) {
            setTimeout(() => createSparkle(), i * 200);
        }

        // Continuous particle generation
        setInterval(createHeart, 800);
        setInterval(createSparkle, 500);

        // Handle NO button hover
        function handleNoHover() {
            const noBtn = document.getElementById('no-btn');
            const container = document.querySelector('.btn-container');
            const containerRect = container.getBoundingClientRect();
            
            const maxX = containerRect.width - noBtn.offsetWidth - 20;
            const maxY = 150;
            
            let newX = Math.random() * maxX;
            let newY = (Math.random() - 0.5) * maxY;
            
            noBtn.style.position = 'absolute';
            noBtn.style.left = newX + 'px';
            noBtn.style.top = newY + 'px';
            noBtn.style.transition = 'all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        }

        // Create confetti
        function createConfetti() {
            const colors = ['#ff2d55', '#ff6b9d', '#ffd700', '#ff8e72', '#fff', '#ff69b4', '#ff1493'];
            
            for (let i = 0; i < 100; i++) {
                setTimeout(() => {
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.left = Math.random() * 100 + 'vw';
                    confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                    confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
                    confetti.style.width = (Math.random() * 10 + 8) + 'px';
                    confetti.style.height = (Math.random() * 10 + 8) + 'px';
                    confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
                    document.body.appendChild(confetti);
                    
                    setTimeout(() => confetti.remove(), 4000);
                }, i * 30);
            }
        }

        // Handle YES click
        function handleYes() {
            document.getElementById('main-container').style.display = 'none';
            
            const celebration = document.createElement('div');
            celebration.className = 'celebration';
            celebration.innerHTML = `
                <div class="side-dancer left">💃</div>
                <div class="side-dancer right">🕺</div>
                <div class="celebration-content">
                    <h1>🎉 YAYYYY!!! 🎉</h1>
                    <h2>Best Choice Ever 💖</h2>
                    <div class="dancers-container">
                        <div class="dancer-wrapper"><span class="dancer">💃</span></div>
                        <div class="dancer-wrapper"><span class="dancer">🕺</span></div>
                        <div class="dancer-wrapper"><span class="dancer">💃</span></div>
                        <div class="dancer-wrapper"><span class="dancer">🕺</span></div>
                        <div class="dancer-wrapper"><span class="dancer">💃</span></div>
                    </div>
                    <div class="emoji-row">🥰 💞 🌹 💘 ✨</div>
                    <p>You just made this Valentine's Day absolutely unforgettable! 😍</p>
                </div>
            `;
            document.body.appendChild(celebration);
            
            createConfetti();
            setInterval(createConfetti, 3000);
        }
    </script>
</body>
</html>
"""

st.components.v1.html(html_content, height=850, scrolling=False)
