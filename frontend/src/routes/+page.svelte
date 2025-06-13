<script>
	let messages = $state([
		{ id: 1, text: "Hello! How can I help you today?", isBot: true, timestamp: new Date() }
	]);
	let inputText = $state('');
	let isTyping = $state(false);

	function sendMessage() {
		if (!inputText.trim()) return;
		
		const userMessage = {
			id: Date.now(),
			text: inputText,
			isBot: false,
			timestamp: new Date()
		};
		messages = [...messages, userMessage];
		
		const userInput = inputText;
		inputText = '';
		isTyping = true;
		
		setTimeout(() => {
			const botMessage = {
				id: Date.now() + 1,
				text: getBotResponse(userInput),
				isBot: true,
				timestamp: new Date()
			};
			messages = [...messages, botMessage];
			isTyping = false;
		}, 1200);
	}

	function getBotResponse(input) {
		const responses = [
			"I understand. Let me help you with that.",
			"That's a great question. Here's what I think:",
			"I can definitely assist you with this.",
			"Let me provide you with some information about that.",
			"That's interesting. Here's my perspective:"
		];
		return responses[Math.floor(Math.random() * responses.length)] + " This is a sample response to demonstrate the interface.";
	}

	function handleKeyPress(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}
</script>

<div class="app">
	<div class="app-container">
		<!-- Left sidebar with branding -->
		<aside class="sidebar">
			<div class="brand">
				<div class="logo">
					<svg width="32" height="32" viewBox="0 0 24 24" fill="none">
						<path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						<path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						<path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
				</div>
				<div class="brand-text">
					<h1>PlotBot</h1>
					<p>Intelligent Conversations</p>
				</div>
			</div>

			<div class="features">
				<div class="feature-item">
					<div class="feature-icon">
						<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
							<path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
					<span>Lightning Fast</span>
				</div>
				<div class="feature-item">
					<div class="feature-icon">
						<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
							<path d="M12 22S8 18 8 13A4 4 0 0 1 16 13C16 18 12 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<path d="M10.5 13A1.5 1.5 0 1 1 13.5 13A1.5 1.5 0 0 1 10.5 13Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
					<span>Secure & Private</span>
				</div>
				<div class="feature-item">
					<div class="feature-icon">
						<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
							<path d="M9 11H15M9 15H15M17 21L12 16L7 21V5A2 2 0 0 1 9 3H15A2 2 0 0 1 17 5V21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
					<span>Smart Responses</span>
				</div>
			</div>

			<div class="stats">
				<div class="stat">
					<div class="stat-number">24/7</div>
					<div class="stat-label">Available</div>
				</div>
				<div class="stat">
					<div class="stat-number">1M+</div>
					<div class="stat-label">Conversations</div>
				</div>
			</div>
		</aside>

		<!-- Main chat area -->
		<main class="main-content">
			<div class="chat-container">
				<header class="header">
					<div class="header-content">
						<div class="bot-info">
							<div class="bot-avatar">
								<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
									<path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							</div>
							<div>
								<h2>Assistant</h2>
								<span class="status">Online</span>
							</div>
						</div>
					</div>
				</header>

				<div class="messages">
					{#each messages as message (message.id)}
						<div class="message {message.isBot ? 'bot' : 'user'}">
							<div class="message-content">
								{message.text}
							</div>
						</div>
					{/each}
					
					{#if isTyping}
						<div class="message bot">
							<div class="message-content typing">
								<div class="typing-indicator">
									<span></span>
									<span></span>
									<span></span>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<footer class="input-area">
					<div class="input-wrapper">
						<textarea
							bind:value={inputText}
							onkeydown={handleKeyPress}
							placeholder="Message Assistant..."
							rows="1"
						></textarea>
						<button 
							onclick={sendMessage} 
							disabled={!inputText.trim()}
							class="send-btn"
							aria-label="Send message"
						>
							<svg width="18" height="18" viewBox="0 0 24 24" fill="none">
								<path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</button>
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
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
		background: #0a0a0a;
		color: #ffffff;
		height: 100vh;
		overflow: hidden;
	}

	.app {
		height: 100vh;
		background: #0a0a0a;
	}

	.app-container {
		display: flex;
		height: 100vh;
		max-width: 1400px;
		margin: 0 auto;
	}

	.sidebar {
		width: 320px;
		background: #0a0a0a;
		padding: 40px 30px;
		display: flex;
		flex-direction: column;
		gap: 40px;
		border-right: 1px solid #1a1a1a;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.logo {
		width: 48px;
		height: 48px;
		background: #ffffff;
		color: #000000;
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.brand-text h1 {
		margin: 0;
		font-size: 24px;
		font-weight: 700;
		color: #ffffff;
		letter-spacing: -0.5px;
	}

	.brand-text p {
		margin: 4px 0 0 0;
		font-size: 14px;
		color: #666666;
	}

	.features {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.feature-item {
		display: flex;
		align-items: center;
		gap: 12px;
		color: #cccccc;
		font-size: 14px;
	}

	.feature-icon {
		width: 32px;
		height: 32px;
		background: #1a1a1a;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #888888;
	}

	.stats {
		display: flex;
		gap: 30px;
		margin-top: auto;
	}

	.stat {
		text-align: left;
	}

	.stat-number {
		font-size: 20px;
		font-weight: 700;
		color: #ffffff;
		margin-bottom: 4px;
	}

	.stat-label {
		font-size: 12px;
		color: #666666;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

	.main-content {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 40px;
		background: #0a0a0a;
	}

	.chat-container {
		width: 100%;
		max-width: 600px;
		height: 100%;
		max-height: 700px;
		background: #111111;
		border-radius: 12px;
		border: 1px solid #222222;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.header {
		padding: 20px 24px;
		border-bottom: 1px solid #222222;
		background: #111111;
	}

	.header-content {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.bot-info {
		display: flex;
		align-items: center;
		gap: 12px;
	}

	.bot-avatar {
		width: 36px;
		height: 36px;
		background: #1a1a1a;
		border: 1px solid #333333;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #888888;
	}

	.bot-info h2 {
		margin: 0;
		font-size: 16px;
		font-weight: 600;
		color: #ffffff;
	}

	.status {
		font-size: 13px;
		color: #22c55e;
	}

	.messages {
		flex: 1;
		overflow-y: auto;
		padding: 24px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.message {
		display: flex;
		max-width: 80%;
	}

	.message.user {
		align-self: flex-end;
	}

	.message.bot {
		align-self: flex-start;
	}

	.message-content {
		padding: 12px 16px;
		border-radius: 18px;
		font-size: 14px;
		line-height: 1.4;
		word-wrap: break-word;
	}

	.message.user .message-content {
		background: #ffffff;
		color: #000000;
	}

	.message.bot .message-content {
		background: #1a1a1a;
		color: #e5e5e5;
		border: 1px solid #2a2a2a;
	}

	.typing {
		padding: 16px !important;
	}

	.typing-indicator {
		display: flex;
		gap: 4px;
		align-items: center;
	}

	.typing-indicator span {
		width: 6px;
		height: 6px;
		background: #666666;
		border-radius: 50%;
		animation: typing 1.4s infinite ease-in-out;
	}

	.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
	.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

	@keyframes typing {
		0%, 80%, 100% { 
			transform: scale(0.8); 
			opacity: 0.5; 
		}
		40% { 
			transform: scale(1); 
			opacity: 1; 
		}
	}

	.input-area {
		padding: 20px 24px;
		border-top: 1px solid #222222;
		background: #111111;
	}

	.input-wrapper {
		display: flex;
		align-items: flex-end;
		gap: 12px;
		background: #1a1a1a;
		border: 1px solid #2a2a2a;
		border-radius: 24px;
		padding: 8px 8px 8px 16px;
		transition: border-color 0.2s ease;
	}

	.input-wrapper:focus-within {
		border-color: #444444;
	}

	textarea {
		flex: 1;
		background: transparent;
		border: none;
		outline: none;
		color: #ffffff;
		font-size: 14px;
		resize: none;
		min-height: 20px;
		max-height: 100px;
		font-family: inherit;
		padding: 8px 0;
	}

	textarea::placeholder {
		color: #666666;
	}

	.send-btn {
		background: #ffffff;
		color: #000000;
		border: none;
		border-radius: 50%;
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.2s ease;
		flex-shrink: 0;
	}

	.send-btn:hover:not(:disabled) {
		background: #f0f0f0;
		transform: scale(1.05);
	}

	.send-btn:disabled {
		background: #333333;
		color: #666666;
		cursor: not-allowed;
		transform: none;
	}

	/* Scrollbar */
	.messages::-webkit-scrollbar {
		width: 4px;
	}

	.messages::-webkit-scrollbar-track {
		background: transparent;
	}

	.messages::-webkit-scrollbar-thumb {
		background: #333333;
		border-radius: 2px;
	}

	.messages::-webkit-scrollbar-thumb:hover {
		background: #444444;
	}

	/* Mobile */
	@media (max-width: 1024px) {
		.app-container {
			flex-direction: column;
		}
		
		.sidebar {
			width: 100%;
			padding: 20px;
			flex-direction: row;
			align-items: center;
			justify-content: space-between;
			border-right: none;
			border-bottom: 1px solid #1a1a1a;
		}
		
		.features, .stats {
			display: none;
		}
		
		.main-content {
			padding: 20px;
		}
	}

	@media (max-width: 768px) {
		.sidebar {
			padding: 16px 20px;
		}
		
		.brand-text h1 {
			font-size: 20px;
		}
		
		.main-content {
			padding: 0;
		}
		
		.chat-container {
			border-radius: 0;
			border: none;
			max-height: none;
		}
		
		.message {
			max-width: 85%;
		}
		
		.header {
			padding: 16px 20px;
		}
		
		.messages {
			padding: 20px;
		}
		
		.input-area {
			padding: 16px 20px;
		}
	}
</style>
