// Configuration
const API_BASE_URL = 'http://localhost:5000/api';
let portfolio = [];

// DOM Elements
const tabBtns = document.querySelectorAll('.nav-btn');
const tabContents = document.querySelectorAll('.tab-content');
const statusIndicator = document.getElementById('statusIndicator');
const loadingSpinner = document.getElementById('loadingSpinner');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    checkAPIHealth();
});

// Tab Navigation
function initializeTabs() {
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            showTab(tabName);
        });
    });
}

function showTab(tabName) {
    // Hide all tabs
    tabContents.forEach(content => {
        content.classList.remove('active');
    });

    // Remove active class from all buttons
    tabBtns.forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked button
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
}

// API Health Check
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            setStatusOnline();
        } else {
            setStatusOffline();
        }
    } catch (error) {
        console.error('API Health Check failed:', error);
        setStatusOffline();
    }
}

function setStatusOnline() {
    const statusText = statusIndicator.querySelector('.status-text');
    const statusDot = statusIndicator.querySelector('.status-dot');
    statusText.textContent = 'En ligne';
    statusDot.classList.remove('error');
}

function setStatusOffline() {
    const statusText = statusIndicator.querySelector('.status-text');
    const statusDot = statusIndicator.querySelector('.status-dot');
    statusText.textContent = 'Hors ligne';
    statusDot.classList.add('error');
}

// Utility Functions
function showLoading() {
    loadingSpinner.style.display = 'flex';
}

function hideLoading() {
    loadingSpinner.style.display = 'none';
}

function displayError(message, resultElementId) {
    const resultElement = document.getElementById(resultElementId);
    resultElement.innerHTML = `<div class="error" style="padding: 1rem; background-color: #fee2e2; border-radius: 0.5rem;">❌ Erreur: ${message}</div>`;
    resultElement.style.display = 'block';
}

// Sentiment Analysis
async function analyzeSentiment() {
    const text = document.getElementById('sentimentText').value;
    
    if (!text.trim()) {
        alert('Veuillez entrer un texte');
        return;
    }

    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}/analyze-sentiment`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        
        if (data.success) {
            displaySentimentResult(data);
        } else {
            displayError(data.error || 'Erreur lors de l\'analyse', 'sentimentResult');
        }
    } catch (error) {
        console.error('Error:', error);
        displayError('Erreur de connexion avec l\'API', 'sentimentResult');
    } finally {
        hideLoading();
    }
}

async function analyzeWithFinBERT() {
    const text = document.getElementById('sentimentText').value;
    
    if (!text.trim()) {
        alert('Veuillez entrer un texte');
        return;
    }

    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}/analyze-financial`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        
        if (data.success) {
            displayFinBERTResult(data);
        } else {
            displayError(data.error || 'Erreur lors de l\'analyse FinBERT', 'sentimentResult');
        }
    } catch (error) {
        console.error('Error:', error);
        displayError('Erreur de connexion avec l\'API', 'sentimentResult');
    } finally {
        hideLoading();
    }
}

function displaySentimentResult(data) {
    const resultBox = document.getElementById('sentimentResult');
    const sentimentLabel = document.getElementById('sentimentLabel');
    const sentimentScore = document.getElementById('sentimentScore');
    const sentimentScoreText = document.getElementById('sentimentScoreText');

    const sentiment = data.sentiment;
    const score = data.score;
    const emoji = sentiment === 'POSITIVE' ? '😊' : '😞';
    const color = sentiment === 'POSITIVE' ? 'var(--success-color)' : 'var(--danger-color)';

    sentimentLabel.innerHTML = `${emoji} ${sentiment}`;
    sentimentLabel.style.color = color;
    
    sentimentScore.style.width = `${score * 100}%`;
    sentimentScore.style.backgroundColor = color;
    sentimentScoreText.textContent = `${Math.round(score * 100)}%`;

    resultBox.style.display = 'block';
}

function displayFinBERTResult(data) {
    const resultBox = document.getElementById('sentimentResult');
    const sentimentLabel = document.getElementById('sentimentLabel');
    const sentimentScore = document.getElementById('sentimentScore');
    const sentimentScoreText = document.getElementById('sentimentScoreText');

    sentimentLabel.innerHTML = `📊 ${data.label}`;
    sentimentLabel.style.color = 'var(--primary-color)';
    
    sentimentScore.style.width = `${data.score * 100}%`;
    sentimentScore.style.backgroundColor = 'var(--primary-color)';
    sentimentScoreText.textContent = `${Math.round(data.score * 100)}%`;

    resultBox.style.display = 'block';
}

// Risk Analysis
async function calculateRisk() {
    const volatility = parseFloat(document.getElementById('volatility').value) || 0;
    const debtRatio = parseFloat(document.getElementById('debtRatio').value) || 0;
    const liquidity = parseFloat(document.getElementById('liquidity').value) || 1;

    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}/calculate-risk`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ volatility, debt_ratio: debtRatio, liquidity })
        });

        const data = await response.json();
        
        if (data.success) {
            displayRiskResult(data);
        } else {
            displayError(data.error || 'Erreur lors du calcul', 'riskResult');
        }
    } catch (error) {
        console.error('Error:', error);
        displayError('Erreur de connexion avec l\'API', 'riskResult');
    } finally {
        hideLoading();
    }
}

function displayRiskResult(data) {
    const resultBox = document.getElementById('riskResult');
    const riskCircle = document.getElementById('riskCircle');
    const riskScoreDisplay = document.getElementById('riskScoreDisplay');
    const riskLevel = document.getElementById('riskLevel');

    const score = data.risk_score;
    const level = data.risk_level;
    
    // Determine color based on risk level
    let color;
    if (level === 'BAS') {
        color = 'var(--success-color)';
    } else if (level === 'MOYEN') {
        color = 'var(--warning-color)';
    } else {
        color = 'var(--danger-color)';
    }

    riskScoreDisplay.textContent = Math.round(score);
    riskScoreDisplay.style.color = color;
    riskCircle.style.borderTop = `4px solid ${color}`;
    riskLevel.textContent = level;
    riskLevel.style.color = color;

    resultBox.style.display = 'block';
}

// Trend Prediction
async function predictTrend() {
    const priceDataStr = document.getElementById('priceData').value;
    
    if (!priceDataStr.trim()) {
        alert('Veuillez entrer les données de prix');
        return;
    }

    const historicalData = priceDataStr.split(',').map(p => parseFloat(p.trim())).filter(p => !isNaN(p));
    
    if (historicalData.length < 2) {
        alert('Veuillez entrer au moins 2 prix');
        return;
    }

    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}/predict-trend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ historical_data: historicalData })
        });

        const data = await response.json();
        
        if (data.success) {
            displayTrendResult(data, historicalData);
        } else {
            displayError(data.error || 'Erreur lors de la prédiction', 'trendResult');
        }
    } catch (error) {
        console.error('Error:', error);
        displayError('Erreur de connexion avec l\'API', 'trendResult');
    } finally {
        hideLoading();
    }
}

function displayTrendResult(data, historicalData) {
    const resultBox = document.getElementById('trendResult');
    const trendDirection = document.getElementById('trendDirection');
    const trendPercent = document.getElementById('trendPercent');
    const trendVolatility = document.getElementById('trendVolatility');

    trendDirection.textContent = data.direction;
    trendPercent.textContent = `${data.trend_percent.toFixed(2)}%`;
    trendVolatility.textContent = `${data.volatility.toFixed(2)}%`;

    drawChart(historicalData);
    resultBox.style.display = 'block';
}

function drawChart(data) {
    const canvas = document.getElementById('trendChart');
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;
    const graphWidth = width - padding * 2;
    const graphHeight = height - padding * 2;

    // Clear canvas
    ctx.fillStyle = '#f9fafb';
    ctx.fillRect(0, 0, width, height);

    // Find min and max values
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;

    // Draw axes
    ctx.strokeStyle = '#d1d5db';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();

    // Draw grid lines
    for (let i = 0; i <= 5; i++) {
        const y = padding + (graphHeight / 5) * i;
        ctx.strokeStyle = '#e5e7eb';
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }

    // Draw data points and line
    const pointSpacing = graphWidth / (data.length - 1 || 1);
    ctx.strokeStyle = '#6366f1';
    ctx.lineWidth = 2;
    ctx.beginPath();

    data.forEach((value, index) => {
        const x = padding + index * pointSpacing;
        const y = height - padding - ((value - min) / range) * graphHeight;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();

    // Draw points
    ctx.fillStyle = '#6366f1';
    data.forEach((value, index) => {
        const x = padding + index * pointSpacing;
        const y = height - padding - ((value - min) / range) * graphHeight;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();
    });

    // Draw labels
    ctx.fillStyle = '#6b7280';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    
    for (let i = 0; i < data.length; i++) {
        if (i % Math.ceil(data.length / 5) === 0 || i === data.length - 1) {
            const x = padding + i * pointSpacing;
            ctx.fillText(`${i}`, x, height - padding + 20);
        }
    }
}

// Portfolio Analysis
function addAsset() {
    const name = document.getElementById('assetName').value;
    const value = parseFloat(document.getElementById('assetValue').value);
    const risk = parseFloat(document.getElementById('assetRisk').value);

    if (!name || isNaN(value) || isNaN(risk)) {
        alert('Veuillez remplir tous les champs correctement');
        return;
    }

    portfolio.push({ name, value, risk });
    updatePortfolioList();

    // Clear inputs
    document.getElementById('assetName').value = '';
    document.getElementById('assetValue').value = '';
    document.getElementById('assetRisk').value = '0.5';
}

function removeAsset(index) {
    portfolio.splice(index, 1);
    updatePortfolioList();
}

function updatePortfolioList() {
    const portfolioList = document.getElementById('portfolioList');
    const analyzeBtn = document.getElementById('analyzeBtn');

    if (portfolio.length === 0) {
        portfolioList.innerHTML = '<p style="text-align: center; color: #9ca3af;">Aucun actif ajouté</p>';
        analyzeBtn.style.display = 'none';
        return;
    }

    portfolioList.innerHTML = portfolio.map((asset, index) => `
        <div class="portfolio-item">
            <div class="portfolio-item-info">
                <div class="portfolio-item-name">${asset.name}</div>
                <div class="portfolio-item-details">
                    Valeur: $${asset.value.toFixed(2)} | Risque: ${asset.risk.toFixed(2)}
                </div>
            </div>
            <button class="portfolio-item-remove" onclick="removeAsset(${index})">Supprimer</button>
        </div>
    `).join('');

    analyzeBtn.style.display = 'block';
}

async function analyzePortfolio() {
    if (portfolio.length === 0) {
        alert('Veuillez ajouter au moins un actif');
        return;
    }

    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}/portfolio-analysis`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ portfolio })
        });

        const data = await response.json();
        
        if (data.success) {
            displayPortfolioResult(data);
        } else {
            displayError(data.error || 'Erreur lors de l\'analyse', 'portfolioResult');
        }
    } catch (error) {
        console.error('Error:', error);
        displayError('Erreur de connexion avec l\'API', 'portfolioResult');
    } finally {
        hideLoading();
    }
}

function displayPortfolioResult(data) {
    const resultBox = document.getElementById('portfolioResult');
    const portfolioTotal = document.getElementById('portfolioTotal');
    const portfolioRisk = document.getElementById('portfolioRisk');
    const allocationChart = document.getElementById('allocationChart');

    portfolioTotal.textContent = `$${data.total_value.toFixed(2)}`;
    portfolioRisk.textContent = data.average_risk.toFixed(2);

    // Create allocation chart
    const chartHTML = data.allocation.map(item => `
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">${item.name}</span>
                <span style="color: #6b7280;">${item.percentage.toFixed(1)}%</span>
            </div>
            <div style="background-color: #e5e7eb; border-radius: 0.5rem; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%); width: ${item.percentage}%; height: 20px;"></div>
            </div>
        </div>
    `).join('');

    allocationChart.innerHTML = chartHTML;
    resultBox.style.display = 'block';
}

// Periodic health check
setInterval(checkAPIHealth, 30000);
