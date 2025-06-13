<script>
	import { marked } from "marked";
	import { onMount } from 'svelte';
	
	let messages = $state([
		{ id: 1, text: marked("Hello! How can I help you today? *All responses are sourced from the internet.*"), isBot: true, timestamp: new Date(), isMarkdown: true }
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
				text: marked(answerText + "\n\n*Response sourced from internet data.*"),
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
	<div class="app-container">
		<aside class="sidebar">
			<div class="sidebar-content">
				<div class="brand">
					<div class="logo">
						<svg width="28" height="28" viewBox="0 0 24 24" fill="none">
							<path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							<path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
					<div class="brand-text">
						<h1>Benny the BA</h1>
						<p>AI Assistant</p>
					</div>
				</div>

				<div class="features">
					<div class="feature-item">
						<div class="feature-icon">⚡</div>
						<div class="feature-text">
							<span class="feature-title">Lightning Fast</span>
							<span class="feature-desc">Instant responses</span>
						</div>
					</div>
					<div class="feature-item">
						<div class="feature-icon">🔒</div>
						<div class="feature-text">
							<span class="feature-title">Secure & Private</span>
							<span class="feature-desc">Your data is safe</span>
						</div>
					</div>
					<div class="feature-item">
						<div class="feature-icon">🤖</div>
						<div class="feature-text">
							<span class="feature-title">Smart AI</span>
							<span class="feature-desc">Advanced reasoning</span>
						</div>
					</div>
					<div class="feature-item">
						<div class="feature-icon">🌐</div>
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
					</div>
					<div class="stat-item">
						<div class="stat-number">24/7</div>
						<div class="stat-label">Available</div>
					</div>
				</div>
			</div>
		</aside>

		<main class="main-content">
			<div class="chat-container">
				<header class="chat-header">
					<div class="header-info">
						<div class="bot-avatar">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
								<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
								<path d="M12 1v6m0 6v6" stroke="currentColor" stroke-width="2"/>
								<path d="m21 12-6-3-6 3-6-3" stroke="currentColor" stroke-width="2"/>
							</svg>
						</div>
						<div class="header-text">
							<h2>Benny</h2>
							<div class="status-indicator">
								<div class="status-dot"></div>
								<span>Online</span>
							</div>
						</div>
					</div>
					<div class="header-actions">
						<button class="action-btn" aria-label="Settings">
							<svg width="18" height="18" viewBox="0 0 24 24" fill="none">
								<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
								<path d="M12 1v6m0 6v6" stroke="currentColor" stroke-width="2"/>
								<path d="m21 12-6-3-6 3-6-3" stroke="currentColor" stroke-width="2"/>
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
										<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
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
								</div>
							</div>
						</div>
					{/each}

					{#if isTyping}
						<div class="message-wrapper bot">
							<div class="message bot">
								<div class="message-avatar">
									<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
										<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
										<path d="M12 1v6m0 6v6" stroke="currentColor" stroke-width="2"/>
									</svg>
								</div>
								<div class="message-bubble typing-bubble">
									<div class="typing-indicator">
										<span></span><span></span><span></span>
									</div>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<footer class="input-area">
					<div class="input-container">
						<div class="input-wrapper">
							<textarea
								bind:this={textareaElement}
								bind:value={inputText}
								onkeydown={handleKeyPress}
								oninput={autoResize}
								placeholder="Type your message..."
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
									<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
										<path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
										<path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
									</svg>
								{/if}
							</button>
						</div>
						<div class="input-hint">
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
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
		background: #0f0f0f;
		color: #ffffff;
		height: 100vh;
		overflow: hidden;
	}

	:global(pre) {
		background: #1a1a1a;
		padding: 12px;
		border-radius: 8px;
		overflow-x: auto;
		border: 1px solid #333;
	}

	:global(code) {
		background: #1a1a1a;
		padding: 2px 6px;
		border-radius: 4px;
		font-size: 0.9em;
	}

	.app {
		height: 100vh;
		background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
	}

	.app-container {
		display: flex;
		height: 100vh;
		max-width: 1600px;
		margin: 0 auto;
	}

	.sidebar {
		width: 350px;
		background: rgba(15, 15, 15, 0.95);
		backdrop-filter: blur(20px);
		border-right: 1px solid rgba(255, 255, 255, 0.1);
		display: flex;
		flex-direction: column;
	}

	.sidebar-content {
		padding: 32px 24px;
		display: flex;
		flex-direction: column;
		gap: 32px;
		height: 100%;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 16px;
		padding: 16px;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 16px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.logo {
		width: 44px;
		height: 44px;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
	}

	.brand-text h1 {
		margin: 0;
		font-size: 22px;
		font-weight: 700;
		color: #ffffff;
		letter-spacing: -0.5px;
	}

	.brand-text p {
		margin: 2px 0 0 0;
		font-size: 13px;
		color: #888;
		font-weight: 500;
	}

	.features {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.feature-item {
		display: flex;
		align-items: center;
		gap: 16px;
		padding: 16px;
		background: rgba(255, 255, 255, 0.03);
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.08);
		transition: all 0.3s ease;
	}

	.feature-item:hover {
		background: rgba(255, 255, 255, 0.06);
		border-color: rgba(255, 255, 255, 0.15);
		transform: translateY(-1px);
	}

	.feature-icon {
		font-size: 20px;
		width: 40px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 10px;
	}

	.feature-text {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.feature-title {
		font-size: 14px;
		font-weight: 600;
		color: #fff;
	}

	.feature-desc {
		font-size: 12px;
		color: #888;
	}

	.stats {
		display: flex;
		gap: 24px;
		margin-top: auto;
		padding: 20px;
		background: rgba(255, 255, 255, 0.03);
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.08);
	}

	.stat-item {
		text-align: center;
	}

	.stat-number {
		font-size: 20px;
		font-weight: 700;
		color: #667eea;
		margin-bottom: 4px;
	}

	.stat-label {
		font-size: 11px;
		color: #888;
		text-transform: uppercase;
		letter-spacing: 0.5px;
		font-weight: 500;
	}

	.main-content {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 24px;
		background: rgba(0, 0, 0, 0.2);
	}

	.chat-container {
		width: 100%;
		max-width: 800px;
		height: 100%;
		max-height: 800px;
		background: rgba(17, 17, 17, 0.95);
		backdrop-filter: blur(20px);
		border-radius: 20px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		display: flex;
		flex-direction: column;
		overflow: hidden;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
	}

	.chat-header {
		padding: 20px 24px;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(255, 255, 255, 0.02);
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.header-info {
		display: flex;
		align-items: center;
		gap: 12px;
	}

	.bot-avatar {
		width: 40px;
		height: 40px;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		border-radius: 10px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
	}

	.header-text h2 {
		margin: 0;
		font-size: 16px;
		font-weight: 600;
		color: #ffffff;
	}

	.status-indicator {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 12px;
		color: #22c55e;
		margin-top: 2px;
	}

	.status-dot {
		width: 6px;
		height: 6px;
		background: #22c55e;
		border-radius: 50%;
		animation: pulse 2s infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.5; }
	}

	.header-actions {
		display: flex;
		gap: 8px;
	}

	.action-btn {
		width: 36px;
		height: 36px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #888;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.action-btn:hover {
		background: rgba(255, 255, 255, 0.1);
		color: #fff;
	}

	.messages {
		flex: 1;
		overflow-y: auto;
		padding: 24px;
		display: flex;
		flex-direction: column;
		gap: 16px;
		scroll-behavior: smooth;
	}

	.message-wrapper {
		display: flex;
		animation: slideIn 0.3s ease-out;
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
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.message {
		display: flex;
		align-items: flex-end;
		gap: 8px;
		max-width: 75%;
	}

	.message-avatar {
		width: 28px;
		height: 28px;
		background: rgba(102, 126, 234, 0.2);
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #667eea;
		flex-shrink: 0;
	}

	.message-bubble {
		position: relative;
		padding: 12px 16px;
		border-radius: 18px;
		font-size: 14px;
		line-height: 1.5;
		word-wrap: break-word;
		word-break: break-word;
		overflow-wrap: break-word;
		hyphens: auto;
		transition: all 0.2s ease;
		max-width: 100%;
		min-width: 0;
		overflow: hidden;
	}

	.message.user .message-bubble {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: #ffffff;
		border-bottom-right-radius: 6px;
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
	}

	.message.bot .message-bubble {
		background: rgba(255, 255, 255, 0.05);
		color: #e5e5e5;
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-bottom-left-radius: 6px;
	}

	.message-content {
		margin-bottom: 4px;
		overflow: hidden;
		word-wrap: break-word;
		word-break: break-word;
		overflow-wrap: anywhere;
		white-space: pre-wrap;
		max-width: 100%;
	}

	.message-time {
		font-size: 11px;
		opacity: 0.6;
		text-align: right;
	}

	.message.bot .message-time {
		text-align: left;
	}

	.typing-bubble {
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
		background: #667eea;
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
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(255, 255, 255, 0.02);
	}

	.input-container {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.input-wrapper {
		display: flex;
		align-items: flex-end;
		gap: 12px;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 20px;
		padding: 12px 16px;
		transition: all 0.2s ease;
	}

	.input-wrapper:focus-within {
		border-color: rgba(102, 126, 234, 0.5);
		box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
		max-height: 120px;
		font-family: inherit;
		padding: 4px 0;
		line-height: 1.5;
	}

	textarea::placeholder {
		color: #666;
	}

	.send-button {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		border: none;
		border-radius: 12px;
		width: 40px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.2s ease;
		flex-shrink: 0;
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
	}

	.send-button:hover:not(:disabled) {
		transform: translateY(-1px);
		box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
	}

	.send-button:disabled {
		background: rgba(255, 255, 255, 0.1);
		color: #666;
		cursor: not-allowed;
		transform: none;
		box-shadow: none;
	}

	.loading-spinner {
		width: 16px;
		height: 16px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-top: 2px solid white;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.input-hint {
		font-size: 11px;
		color: #666;
		text-align: center;
		opacity: 0.8;
	}

	/* Scrollbar */
	.messages::-webkit-scrollbar {
		width: 6px;
	}

	.messages::-webkit-scrollbar-track {
		background: transparent;
	}

	.messages::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.2);
		border-radius: 3px;
	}

	.messages::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.3);
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
			padding: 16px 20px;
		}
		
		.features, .stats {
			display: none;
		}
		
		.main-content {
			padding: 16px;
		}

		.chat-container {
			max-height: none;
			border-radius: 16px;
		}
	}

	@media (max-width: 768px) {
		.sidebar-content {
			padding: 12px 16px;
		}
		
		.brand-text h1 {
			font-size: 18px;
		}
		
		.main-content {
			padding: 8px;
		}
		
		.chat-container {
			border-radius: 12px;
		}
		
		.message {
			max-width: 85%;
		}
		
		.chat-header {
			padding: 16px 20px;
		}
		
		.messages {
			padding: 16px;
		}
		
		.input-area {
			padding: 16px 20px;
		}
	}

	/* Fix for markdown content inside message bubbles */
	.message-content :global(p) {
		margin: 0;
		background: none !important;
		padding: 0 !important;
		border: none !important;
		word-wrap: break-word;
		white-space: pre-wrap;
	}

	.message-content :global(p:first-child) {
		margin-top: 0;
	}

	.message-content :global(p:last-child) {
		margin-bottom: 0;
	}

	/* Ensure all markdown elements don't have conflicting backgrounds */
	.message-content :global(*) {
		background: transparent !important;
	}

	/* Fix code blocks inside messages */
	.message-content :global(pre) {
		background: rgba(0, 0, 0, 0.3) !important;
		margin: 8px 0;
	}

	.message-content :global(code) {
		background: rgba(0, 0, 0, 0.2) !important;
	}

/* Aggressive overflow prevention for all message content */
.message-content :global(*) {
	max-width: 100% !important;
	overflow: hidden !important;
	word-wrap: break-word !important;
	word-break: break-word !important;
	overflow-wrap: anywhere !important;
	white-space: pre-wrap !important;
}

/* Special handling for code blocks to prevent horizontal scroll */
.message-content :global(pre) {
	background: rgba(0, 0, 0, 0.3) !important;
	margin: 8px 0;
	overflow-x: hidden !important;
	white-space: pre-wrap !important;
	word-wrap: break-word !important;
	word-break: break-all !important;
}

.message-content :global(code) {
	background: rgba(0, 0, 0, 0.2) !important;
	white-space: pre-wrap !important;
	word-wrap: break-word !important;
	word-break: break-all !important;
}

/* Handle long URLs and links */
.message-content :global(a) {
	word-break: break-all !important;
	overflow-wrap: anywhere !important;
}

/* Handle tables if any */
.message-content :global(table) {
	width: 100% !important;
	table-layout: fixed !important;
	word-wrap: break-word !important;
}

.message-content :global(td), 
.message-content :global(th) {
	word-wrap: break-word !important;
	word-break: break-word !important;
	overflow: hidden !important;
}
</style>
