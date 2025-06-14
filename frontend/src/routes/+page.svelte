<script>
	import { marked } from "marked";
	import { onMount } from 'svelte';
	
	let messages = $state([
		{ id: 1, text: marked("Hello! How can I help you today? ✨ *All responses are sourced from the internet.*"), isBot: true, timestamp: new Date(), isMarkdown: true }
	]);
	let inputText = $state('');
	let isTyping = $state(false);
	let messagesContainer = $state();
	let textareaElement = $state();

	// Auto-scroll to bottom when new messages arrive
	function autoScroll() {
		if (messagesContainer && messages.length > 0) {
			setTimeout(() => {
				messagesContainer.scrollTop = messagesContainer.scrollHeight;
			}, 100);
		}
	}

	// Auto-resize textarea
	function autoResize() {
		if (textareaElement) {
			textareaElement.style.height = 'auto';
			textareaElement.style.height = Math.min(textareaElement.scrollHeight, 120) + 'px';
		}
	}

	async function sendMessage() {
		if (!inputText.trim()) return;

		const userMessage = {
			id: Date.now(),
			text: inputText,
			isBot: false,
			timestamp: new Date(),
			isMarkdown: false
		};
		messages = [...messages, userMessage];

		const userInput = inputText;
		inputText = '';
		autoResize();
		isTyping = true;

		try {
			const response = await fetch("http://localhost:8000/ask", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ question: userInput })
			});

			const data = await response.json();
			const answerText = data.answer || "No response from AI.";

			const botMessage = {
				id: Date.now() + 1,
				text: marked(answerText + "\n\n*✨ Response sourced from internet data.*"),
				isBot: true,
				timestamp: new Date(),
				isMarkdown: true
			};
			messages = [...messages, botMessage];
		} catch (error) {
			messages = [
				...messages,
				{
					id: Date.now() + 2,
					text: "⚠️ Error: " + error.message,
					isBot: true,
					timestamp: new Date(),
					isMarkdown: false
				}
			];
		} finally {
			isTyping = false;
			autoScroll();
		}
	}

	function handleKeyPress(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}

	function formatTime(date) {
		return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}

	onMount(() => {
		autoResize();
	});
</script>

<div class="app">
	<div class="background-effects">
		<div class="gradient-orb orb-1"></div>
		<div class="gradient-orb orb-2"></div>
		<div class="gradient-orb orb-3"></div>
	</div>
	
	<div class="app-container">
		<aside class="sidebar">
			<div class="sidebar-content">
				<div class="brand">
					<div class="logo">
						<svg width="32" height="32" viewBox="0 0 24 24" fill="none">
							<path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
					<div class="brand-text">
						<h1>Benny the BA</h1>
						<p>AI Assistant</p>
					</div>
					<div class="brand-glow"></div>
				</div>

				<div class="features">
					<div class="feature-item">
						<div class="feature-icon lightning">⚡</div>
						<div class="feature-text">
							<span class="feature-title">Lightning Fast</span>
							<span class="feature-desc">Instant responses</span>
						</div>
					</div>
					<div class="feature-item">
						<div class="feature-icon secure">🔒</div>
						<div class="feature-text">
							<span class="feature-title">Secure & Private</span>
							<span class="feature-desc">Your data is safe</span>
						</div>
					</div>
					<div class="feature-item">
						<div class="feature-icon smart">🤖</div>
						<div class="feature-text">
							<span class="feature-title">Smart AI</span>
							<span class="feature-desc">Advanced reasoning</span>
						</div>
					</div>
					<div class="feature-item">
						<div class="feature-icon internet">🌐</div>
						<div class="feature-text">
							<span class="feature-title">Internet Sourced</span>
							<span class="feature-desc">All responses from web</span>
						</div>
					</div>
				</div>

				<div class="stats">
					<div class="stat-item">
						<div class="stat-number">{messages.length}</div>
						<div class="stat-label">Messages</div>
						<div class="stat-glow"></div>
					</div>
					<div class="stat-item">
						<div class="stat-number">24/7</div>
						<div class="stat-label">Available</div>
						<div class="stat-glow"></div>
					</div>
				</div>
			</div>
		</aside>

		<main class="main-content">
			<div class="chat-container">
				<header class="chat-header">
					<div class="header-info">
						<div class="bot-avatar">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
								<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
								<path d="M12 1v6m0 6v6" stroke="currentColor" stroke-width="2"/>
								<path d="m21 12-6-3-6 3-6-3" stroke="currentColor" stroke-width="2"/>
							</svg>
							<div class="avatar-glow"></div>
						</div>
						<div class="header-text">
							<h2>Benny</h2>
							<div class="status-indicator">
								<div class="status-dot"></div>
								<span>Online & Ready</span>
							</div>
						</div>
					</div>
					<div class="header-actions">
						<button class="action-btn" aria-label="Settings">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
								<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
								<path d="M12 1v6m0 6v6" stroke="currentColor" stroke-width="2"/>
								<path d="m21 12-6-3-6 3-6-3" stroke="currentColor" stroke-width="2"/>
							</svg>
						</button>
						<button class="action-btn" aria-label="More options">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
								<circle cx="12" cy="12" r="1" stroke="currentColor" stroke-width="2"/>
								<circle cx="19" cy="12" r="1" stroke="currentColor" stroke-width="2"/>
								<circle cx="5" cy="12" r="1" stroke="currentColor" stroke-width="2"/>
							</svg>
						</button>
					</div>
				</header>

				<div class="messages" bind:this={messagesContainer}>
					{#each messages as message (message.id)}
						<div class="message-wrapper" class:user={!message.isBot} class:bot={message.isBot}>
							<div class="message" class:user={!message.isBot} class:bot={message.isBot}>
								{#if message.isBot}
									<div class="message-avatar">
										<svg width="18" height="18" viewBox="0 0 24 24" fill="none">
											<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
											<path d="M12 1v6m0 6v6" stroke="currentColor" stroke-width="2"/>
										</svg>
									</div>
								{/if}
								<div class="message-bubble">
									{#if message.isMarkdown}
										<div class="message-content">{@html message.text}</div>
									{:else}
										<div class="message-content">{message.text}</div>
									{/if}
									<div class="message-time">{formatTime(message.timestamp)}</div>
									<div class="message-glow"></div>
								</div>
							</div>
						</div>
					{/each}

					{#if isTyping}
						<div class="message-wrapper bot">
							<div class="message bot">
								<div class="message-avatar">
									<svg width="18" height="18" viewBox="0 0 24 24" fill="none">
										<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
										<path d="M12 1v6m0 6v6" stroke="currentColor" stroke-width="2"/>
									</svg>
								</div>
								<div class="message-bubble typing-bubble">
									<div class="typing-indicator">
										<span></span><span></span><span></span>
									</div>
									<div class="typing-text">Benny is thinking...</div>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<footer class="input-area">
					<div class="input-container">
						<div class="input-wrapper">
							<div class="input-glow"></div>
							<textarea
								bind:this={textareaElement}
								bind:value={inputText}
								onkeydown={handleKeyPress}
								oninput={autoResize}
								placeholder="Ask me anything..."
								rows="1"
							></textarea>
							<button 
								class="send-button" 
								onclick={sendMessage} 
								disabled={!inputText.trim() || isTyping} 
								aria-label="Send message"
							>
								{#if isTyping}
									<div class="loading-spinner"></div>
								{:else}
									<svg width="22" height="22" viewBox="0 0 24 24" fill="none">
										<path d="M22 2L11 13" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
										<path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
									</svg>
								{/if}
								<div class="send-glow"></div>
							</button>
						</div>
						<div class="input-hint">
							<span class="hint-icon">💡</span>
							Press Enter to send, Shift + Enter for new line • All responses sourced from internet
						</div>
					</div>
				</footer>
			</div>
		</main>
	</div>
</div>

<style>
	:global(*) {
		box-sizing: border-box;
	}

	:global(body) {
		margin: 0;
		padding: 0;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Inter', sans-serif;
		background: #000000;
		color: #ffffff;
		height: 100vh;
		overflow: hidden;
		font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
	}

	:global(pre) {
		background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
		padding: 16px;
		border-radius: 12px;
		overflow-x: auto;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
	}

	:global(code) {
		background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
		padding: 4px 8px;
		border-radius: 6px;
		font-size: 0.9em;
		border: 1px solid rgba(255, 255, 255, 0.05);
	}

	.app {
		height: 100vh;
		background: radial-gradient(ellipse at top, #1a1a1a 0%, #0d0d0d 25%, #050505 50%, #000000 100%);
		position: relative;
		overflow: hidden;
	}

	.background-effects {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: 0;
	}

	.gradient-orb {
		position: absolute;
		border-radius: 50%;
		filter: blur(60px);
		opacity: 0.3;
		animation: float 6s ease-in-out infinite;
	}

	.orb-1 {
		width: 300px;
		height: 300px;
		background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%);
		top: -150px;
		left: -150px;
		animation-delay: 0s;
	}

	.orb-2 {
		width: 200px;
		height: 200px;
		background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%);
		top: 50%;
		right: -100px;
		animation-delay: 2s;
	}

	.orb-3 {
		width: 250px;
		height: 250px;
		background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%);
		bottom: -125px;
		left: 30%;
		animation-delay: 4s;
	}

	@keyframes float {
		0%, 100% { transform: translateY(0px) rotate(0deg); }
		33% { transform: translateY(-20px) rotate(120deg); }
		66% { transform: translateY(10px) rotate(240deg); }
	}

	.app-container {
		display: flex;
		height: 100vh;
		max-width: 1600px;
		margin: 0 auto;
		position: relative;
		z-index: 1;
	}

	.sidebar {
		width: 380px;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(40px);
		border-right: 1px solid rgba(255, 255, 255, 0.1);
		display: flex;
		flex-direction: column;
		position: relative;
	}

	.sidebar::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%);
		pointer-events: none;
	}

	.sidebar-content {
		padding: 40px 28px;
		display: flex;
		flex-direction: column;
		gap: 36px;
		height: 100%;
		position: relative;
		z-index: 1;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 20px;
		padding: 24px;
		background: rgba(255, 255, 255, 0.03);
		backdrop-filter: blur(20px);
		border-radius: 20px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		position: relative;
		overflow: hidden;
		transition: all 0.3s ease;
	}

	.brand:hover {
		transform: translateY(-2px);
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
		border-color: rgba(255, 255, 255, 0.2);
	}

	.brand-glow {
		position: absolute;
		top: -50%;
		left: -50%;
		width: 200%;
		height: 200%;
		background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.05), transparent);
		animation: rotate 3s linear infinite;
		pointer-events: none;
	}

	@keyframes rotate {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.logo {
		width: 52px;
		height: 52px;
		background: linear-gradient(135deg, #333333 0%, #1a1a1a 50%, #000000 100%);
		border-radius: 16px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
		position: relative;
		z-index: 1;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.brand-text h1 {
		margin: 0;
		font-size: 26px;
		font-weight: 800;
		color: #ffffff;
		letter-spacing: -0.8px;
		background: linear-gradient(135deg, #ffffff 0%, #cccccc 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.brand-text p {
		margin: 4px 0 0 0;
		font-size: 14px;
		color: #888888;
		font-weight: 600;
		letter-spacing: 0.5px;
	}

	.features {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.feature-item {
		display: flex;
		align-items: center;
		gap: 20px;
		padding: 20px;
		background: rgba(255, 255, 255, 0.02);
		backdrop-filter: blur(20px);
		border-radius: 16px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
		position: relative;
		overflow: hidden;
	}

	.feature-item::before {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
		transition: left 0.5s ease;
	}

	.feature-item:hover::before {
		left: 100%;
	}

	.feature-item:hover {
		background: rgba(255, 255, 255, 0.05);
		border-color: rgba(255, 255, 255, 0.15);
		transform: translateY(-3px) scale(1.02);
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
	}

	.feature-icon {
		font-size: 24px;
		width: 48px;
		height: 48px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 12px;
		position: relative;
		transition: all 0.3s ease;
	}

	.feature-icon.lightning {
		background: linear-gradient(135deg, #ffd700 0%, #ffb347 100%);
		box-shadow: 0 8px 24px rgba(255, 215, 0, 0.3);
		color: #000;
	}

	.feature-icon.secure {
		background: linear-gradient(135deg, #c0c0c0 0%, #808080 100%);
		box-shadow: 0 8px 24px rgba(192, 192, 192, 0.3);
		color: #000;
	}

	.feature-icon.smart {
		background: linear-gradient(135deg, #ffffff 0%, #cccccc 100%);
		box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2);
		color: #000;
	}

	.feature-icon.internet {
		background: linear-gradient(135deg, #666666 0%, #333333 100%);
		box-shadow: 0 8px 24px rgba(102, 102, 102, 0.3);
		color: #fff;
	}

	.feature-text {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.feature-title {
		font-size: 16px;
		font-weight: 700;
		color: #ffffff;
		letter-spacing: -0.2px;
	}

	.feature-desc {
		font-size: 13px;
		color: #888888;
		font-weight: 500;
	}

	.stats {
		display: flex;
		gap: 28px;
		margin-top: auto;
		padding: 24px;
		background: rgba(255, 255, 255, 0.02);
		backdrop-filter: blur(20px);
		border-radius: 16px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		position: relative;
	}

	.stat-item {
		text-align: center;
		position: relative;
		flex: 1;
	}

	.stat-glow {
		position: absolute;
		top: -10px;
		left: 50%;
		transform: translateX(-50%);
		width: 60px;
		height: 4px;
		background: linear-gradient(90deg, transparent, #ffffff, transparent);
		border-radius: 2px;
		opacity: 0.4;
		animation: pulse 2s ease-in-out infinite;
	}

	.stat-number {
		font-size: 24px;
		font-weight: 800;
		background: linear-gradient(135deg, #ffffff 0%, #cccccc 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		margin-bottom: 6px;
		letter-spacing: -0.5px;
	}

	.stat-label {
		font-size: 12px;
		color: #888888;
		text-transform: uppercase;
		letter-spacing: 1px;
		font-weight: 600;
	}

	.main-content {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 32px;
		background: rgba(0, 0, 0, 0.2);
	}

	.chat-container {
		width: 100%;
		max-width: 900px;
		height: 100%;
		max-height: 850px;
		background: rgba(0, 0, 0, 0.7);
		backdrop-filter: blur(40px);
		border-radius: 24px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		display: flex;
		flex-direction: column;
		overflow: hidden;
		box-shadow: 0 32px 64px rgba(0, 0, 0, 0.6);
		position: relative;
	}

	.chat-container::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.01) 0%, rgba(255, 255, 255, 0.005) 100%);
		pointer-events: none;
	}

	.chat-header {
		padding: 24px 32px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(255, 255, 255, 0.02);
		display: flex;
		align-items: center;
		justify-content: space-between;
		position: relative;
		z-index: 1;
	}

	.header-info {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.bot-avatar {
		width: 48px;
		height: 48px;
		background: linear-gradient(135deg, #333333 0%, #1a1a1a 50%, #000000 100%);
		border-radius: 14px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
		position: relative;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

.avatar-glow {
		position: absolute;
		top: -2px;
		left: -2px;
		right: -2px;
		bottom: -2px;
		background: linear-gradient(135deg, #ffffff, #cccccc, #999999);
		border-radius: 16px;
		z-index: -1;
		opacity: 0.3;
		animation: pulse 2s infinite;
	}

	.header-text h2 {
		margin: 0;
		font-size: 20px;
		font-weight: 700;
		color: #ffffff;
		letter-spacing: -0.3px;
	}

	.status-indicator {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 13px;
		color: #00ff88;
		margin-top: 4px;
		font-weight: 600;
	}

	.status-dot {
		width: 8px;
		height: 8px;
		background: #00ff88;
		border-radius: 50%;
		animation: pulse 2s infinite;
		box-shadow: 0 0 10px #00ff88;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; transform: scale(1); }
		50% { opacity: 0.7; transform: scale(1.1); }
	}

	.header-actions {
		display: flex;
		gap: 12px;
	}

	.action-btn {
		width: 44px;
		height: 44px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #888888;
		cursor: pointer;
		transition: all 0.3s ease;
		backdrop-filter: blur(10px);
	}

	.action-btn:hover {
		background: rgba(255, 255, 255, 0.1);
		color: #ffffff;
		border-color: rgba(255, 255, 255, 0.2);
		transform: translateY(-2px);
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
	}

	.messages {
		flex: 1;
		overflow-y: auto;
		padding: 32px;
		display: flex;
		flex-direction: column;
		gap: 20px;
		scroll-behavior: smooth;
		position: relative;
		z-index: 1;
	}

	.message-wrapper {
		display: flex;
		animation: slideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.message-wrapper.user {
		justify-content: flex-end;
	}

	.message-wrapper.bot {
		justify-content: flex-start;
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateY(20px) scale(0.95);
		}
		to {
			opacity: 1;
			transform: translateY(0) scale(1);
		}
	}

	.message {
		display: flex;
		align-items: flex-end;
		gap: 12px;
		max-width: 80%;
	}

	.message-avatar {
		width: 32px;
		height: 32px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 10px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #ffffff;
		flex-shrink: 0;
		border: 1px solid rgba(255, 255, 255, 0.15);
	}

	.message-bubble {
		position: relative;
		padding: 16px 20px;
		border-radius: 20px;
		font-size: 15px;
		line-height: 1.6;
		word-wrap: break-word;
		word-break: break-word;
		overflow-wrap: break-word;
		hyphens: auto;
		transition: all 0.3s ease;
		max-width: 100%;
		min-width: 0;
		overflow: hidden;
		backdrop-filter: blur(20px);
	}

	.message.user .message-bubble {
		background: linear-gradient(135deg, #333333 0%, #1a1a1a 50%, #000000 100%);
		color: #ffffff;
		border-bottom-right-radius: 8px;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
		border: 1px solid rgba(255, 255, 255, 0.2);
	}

	.message.bot .message-bubble {
		background: rgba(255, 255, 255, 0.05);
		color: #e5e7eb;
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-bottom-left-radius: 8px;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
	}

	.message-glow {
		position: absolute;
		top: -1px;
		left: -1px;
		right: -1px;
		bottom: -1px;
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
		border-radius: 21px;
		z-index: -1;
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.message-bubble:hover .message-glow {
		opacity: 1;
	}

	.message-content {
		margin-bottom: 8px;
		overflow: hidden;
		word-wrap: break-word;
		word-break: break-word;
		overflow-wrap: anywhere;
		white-space: pre-wrap;
		max-width: 100%;
	}

	.message-time {
		font-size: 11px;
		opacity: 0.7;
		text-align: right;
		font-weight: 500;
		letter-spacing: 0.3px;
	}

	.message.bot .message-time {
		text-align: left;
	}

	.typing-bubble {
		padding: 20px !important;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.typing-indicator {
		display: flex;
		gap: 6px;
		align-items: center;
	}

	.typing-indicator span {
		width: 8px;
		height: 8px;
		background: linear-gradient(135deg, #ffffff 0%, #cccccc 100%);
		border-radius: 50%;
		animation: typing 1.4s infinite ease-in-out;
		box-shadow: 0 2px 8px rgba(255, 255, 255, 0.2);
	}

	.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
	.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

	.typing-text {
		font-size: 12px;
		color: #888888;
		font-style: italic;
		font-weight: 500;
	}

	@keyframes typing {
		0%, 80%, 100% { 
			transform: scale(0.8); 
			opacity: 0.5; 
		}
		40% { 
			transform: scale(1.2); 
			opacity: 1; 
		}
	}

	.input-area {
		padding: 24px 32px 32px;
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(255, 255, 255, 0.02);
		position: relative;
		z-index: 1;
	}

	.input-container {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.input-wrapper {
		display: flex;
		align-items: flex-end;
		gap: 16px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 24px;
		padding: 16px 20px;
		transition: all 0.3s ease;
		position: relative;
		backdrop-filter: blur(20px);
	}

	.input-glow {
		position: absolute;
		top: -1px;
		left: -1px;
		right: -1px;
		bottom: -1px;
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
		border-radius: 25px;
		z-index: -1;
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.input-wrapper:focus-within {
		border-color: rgba(255, 255, 255, 0.3);
		box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.05);
		background: rgba(255, 255, 255, 0.08);
	}

	.input-wrapper:focus-within .input-glow {
		opacity: 1;
	}

	textarea {
		flex: 1;
		background: transparent;
		border: none;
		outline: none;
		color: #ffffff;
		font-size: 15px;
		resize: none;
		min-height: 24px;
		max-height: 120px;
		font-family: inherit;
		padding: 4px 0;
		line-height: 1.6;
		font-weight: 500;
	}

	textarea::placeholder {
		color: #666666;
		font-weight: 500;
	}

	.send-button {
		background: linear-gradient(135deg, #333333 0%, #1a1a1a 50%, #000000 100%);
		color: white;
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		width: 48px;
		height: 48px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.3s ease;
		flex-shrink: 0;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
		position: relative;
		overflow: hidden;
	}

	.send-glow {
		position: absolute;
		top: -2px;
		left: -2px;
		right: -2px;
		bottom: -2px;
		background: linear-gradient(135deg, #ffffff, #cccccc, #999999);
		border-radius: 18px;
		z-index: -1;
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.send-button:hover:not(:disabled) {
		transform: translateY(-2px) scale(1.05);
		box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
		border-color: rgba(255, 255, 255, 0.4);
	}

	.send-button:hover:not(:disabled) .send-glow {
		opacity: 0.5;
	}

	.send-button:disabled {
		background: rgba(255, 255, 255, 0.05);
		color: #666666;
		cursor: not-allowed;
		transform: none;
		box-shadow: none;
		border-color: rgba(255, 255, 255, 0.05);
	}

	.loading-spinner {
		width: 20px;
		height: 20px;
		border: 2.5px solid rgba(255, 255, 255, 0.3);
		border-top: 2.5px solid white;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.input-hint {
		font-size: 12px;
		color: #666666;
		text-align: center;
		opacity: 0.9;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		font-weight: 500;
	}

	.hint-icon {
		font-size: 14px;
	}

	/* Enhanced Scrollbar */
	.messages::-webkit-scrollbar {
		width: 8px;
	}

	.messages::-webkit-scrollbar-track {
		background: rgba(255, 255, 255, 0.05);
		border-radius: 4px;
	}

	.messages::-webkit-scrollbar-thumb {
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.2));
		border-radius: 4px;
		transition: background 0.3s ease;
	}

	.messages::-webkit-scrollbar-thumb:hover {
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.3));
	}

	/* Mobile Responsive */
	@media (max-width: 1024px) {
		.app-container {
			flex-direction: column;
		}
		
		.sidebar {
			width: 100%;
			height: auto;
			border-right: none;
			border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		}

		.sidebar-content {
			flex-direction: row;
			align-items: center;
			justify-content: space-between;
			padding: 20px 24px;
		}
		
		.features, .stats {
			display: none;
		}
		
		.main-content {
			padding: 20px;
		}

		.chat-container {
			max-height: none;
			border-radius: 20px;
		}
	}

	@media (max-width: 768px) {
		.sidebar-content {
			padding: 16px 20px;
		}
		
		.brand-text h1 {
			font-size: 20px;
		}
		
		.main-content {
			padding: 12px;
		}
		
		.chat-container {
			border-radius: 16px;
		}
		
		.message {
			max-width: 90%;
		}
		
		.chat-header {
			padding: 20px 24px;
		}
		
		.messages {
			padding: 20px;
		}
		
		.input-area {
			padding: 20px 24px 24px;
		}

		.gradient-orb {
			display: none;
		}
	}

	/* Enhanced markdown content styling */
	.message-content :global(p) {
		margin: 0 0 8px 0;
		background: none !important;
		padding: 0 !important;
		border: none !important;
		word-wrap: break-word;
		white-space: pre-wrap;
	}

	.message-content :global(p:last-child) {
		margin-bottom: 0;
	}

	.message-content :global(*) {
		background: transparent !important;
	}

	.message-content :global(pre) {
		background: linear-gradient(135deg, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0.8) 100%) !important;
		margin: 12px 0;
		border: 1px solid rgba(255, 255, 255, 0.1) !important;
	}

	.message-content :global(code) {
		background: linear-gradient(135deg, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.6) 100%) !important;
		border: 1px solid rgba(255, 255, 255, 0.05) !important;
	}

	.message-content :global(a) {
		color: #ffffff;
		text-decoration: none;
		border-bottom: 1px solid rgba(255, 255, 255, 0.3);
		transition: all 0.2s ease;
	}

	.message-content :global(a:hover) {
		color: #cccccc;
		border-bottom-color: rgba(204, 204, 204, 0.6);
	}

	/* Overflow prevention */
	.message-content :global(*) {
		max-width: 100% !important;
		overflow: hidden !important;
		word-wrap: break-word !important;
		word-break: break-word !important;
		overflow-wrap: anywhere !important;
		white-space: pre-wrap !important;
	}

	.message-content :global(pre) {
		overflow-x: hidden !important;
		white-space: pre-wrap !important;
		word-wrap: break-word !important;
		word-break: break-all !important;
	}

	.message-content :global(table) {
		width: 100% !important;
		table-layout: fixed !important;
		word-wrap: break-word !important;
		border-collapse: collapse;
		border: 1px solid rgba(255, 255, 255, 0.1) !important;
		border-radius: 8px;
		overflow: hidden;
	}

	.message-content :global(td), 
	.message-content :global(th) {
		word-wrap: break-word !important;
		word-break: break-word !important;
		overflow: hidden !important;
		padding: 8px 12px;
		border: 1px solid rgba(255, 255, 255, 0.05) !important;
	}

	.message-content :global(th) {
		background: rgba(255, 255, 255, 0.05) !important;
		font-weight: 600;
	}
</style>
