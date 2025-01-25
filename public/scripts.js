let currentCardIndex = 0;

async function startLearning() {
    const topic = document.getElementById('topic').value;
    if (!topic) return alert('请输入学习主题！');

    try {
        const response = await fetch(`/api/generate?topic=${encodeURIComponent(topic)}`);
        const cards = await response.json();
        currentCardIndex = 0;
        renderCard(cards[currentCardIndex]);
    } catch (error) {
        alert('生成失败: ' + error.message);
    }
}

function renderCard(card) {
    const container = document.getElementById('card-container');
    container.innerHTML = `
        <div class="card">
            <h2>${card.title}</h2>
            <div class="knowledge">${card.knowledge}</div>
            <div class="questions">
                ${card.questions.map((q, i) => `
                    <div class="question">
                        <p>❓ 问题 ${i+1}: ${q.q}</p>
                        <textarea id="answer-${i}"></textarea>
                        <button onclick="showAnswer(${i})">显示答案</button>
                        <p class="answer" id="answer-${i}-ref" style="display:none">💡 参考答案: ${q.a}</p>
                    </div>
                `).join('')}
            </div>
            <button onclick="nextCard()">下一题</button>
        </div>
    `;
}

function showAnswer(index) {
    document.getElementById(`answer-${index}-ref`).style.display = 'block';
}

async function nextCard() {
    // 这里可以添加保存评分逻辑
    currentCardIndex++;
    const response = await fetch(`/api/generate?topic=${document.getElementById('topic').value}`);
    const cards = await response.json();
    if (currentCardIndex < cards.length) {
        renderCard(cards[currentCardIndex]);
    } else {
        document.getElementById('card-container').innerHTML = '<p>🎉 学习完成！</p>';
    }
}