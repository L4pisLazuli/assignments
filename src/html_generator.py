"""
HTML生成モジュール
"""
from datetime import datetime
from utils import calculate_urgency


def generate_html(assignments, messages_with_subject, logger):
    """WebClass情報をHTMLとして生成する"""
    try:
        # 重複を排除し、期限順にソート
        from utils import deduplicate_assignments
        unique_assignments = deduplicate_assignments(assignments)
        
        logger.info(f"課題数: {len(unique_assignments)}")
        logger.info(f"お知らせ数: {len(messages_with_subject)}")
        
        html = _get_html_template()
        
        # 課題セクションの生成
        assignments_html = _generate_assignments_html(unique_assignments)
        
        # お知らせセクションの生成
        messages_html = _generate_messages_html(messages_with_subject)
        
        # HTMLを組み立て
        html = html.replace("{{ASSIGNMENTS}}", assignments_html)
        html = html.replace("{{MESSAGES}}", messages_html)
        
        return html
    except Exception as e:
        logger.error(f"HTML生成中にエラーが発生しました: {e}")
        raise


def _generate_assignments_html(assignments):
    """課題一覧のHTMLを生成"""
    html = ""
    for assignment in assignments:
        due_date = assignment.get('availability_period_to', '')
        urgency_class = calculate_urgency(due_date)
        assignment_id = f"{assignment.get('subject', '')}_{assignment.get('name', '')}"
        
        html += f"""
            <div class="assignment {urgency_class} uncompleted" data-assignment-id="{assignment_id}">
                <input type="checkbox" class="checkbox assignment-checkbox">
                <span class="subject">{assignment.get('subject', '')}</span>
                <span class="title">{assignment.get('name', '')}</span>
                <span class="category">{assignment.get('category', '')}</span>
                <div class="due-date">期限: {due_date}</div>
            </div>
        """
    return html


def _generate_messages_html(messages_with_subject):
    """お知らせ一覧のHTMLを生成"""
    # お知らせを科目名でソート
    messages_with_subject.sort(key=lambda x: x[0])
    
    html = ""
    for subject, message in messages_with_subject:
        message_id = f"{subject}_{message}"
        html += f"""
            <div class="message" data-message-id="{message_id}">
                <span class="message-subject">{subject}</span>
                <div class="message-divider"></div>
                <p class="message-content">{message}</p>
            </div>
        """
    return html


def _get_html_template():
    """HTMLテンプレートを取得"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WebClass情報</title>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --md-sys-color-primary: #0061a4;
                --md-sys-color-primary-container: #d1e4ff;
                --md-sys-color-secondary: #535f70;
                --md-sys-color-secondary-container: #d7e3f8;
                --md-sys-color-tertiary: #6b5778;
                --md-sys-color-tertiary-container: #f3daff;
                --md-sys-color-error: #ba1a1a;
                --md-sys-color-error-container: #ffdad6;
                --md-sys-color-surface: #fdfcff;
                --md-sys-color-surface-variant: #dfe2eb;
                --md-sys-color-outline: #73777f;
                --md-sys-color-outline-variant: #c3c7cf;
                --md-sys-color-shadow: #000000;
                --md-sys-color-scrim: #000000;
                --md-sys-color-inverse-surface: #2f3033;
                --md-sys-color-inverse-on-surface: #f1f0f4;
                --md-sys-color-inverse-primary: #9fcaee;
                --md-sys-color-surface-tint: #0061a4;
                --md-sys-color-on-primary: #ffffff;
                --md-sys-color-on-primary-container: #001d36;
                --md-sys-color-on-secondary: #ffffff;
                --md-sys-color-on-secondary-container: #101c2b;
                --md-sys-color-on-tertiary: #ffffff;
                --md-sys-color-on-tertiary-container: #251431;
                --md-sys-color-on-error: #ffffff;
                --md-sys-color-on-error-container: #410002;
                --md-sys-color-on-surface: #1a1c1e;
                --md-sys-color-on-surface-variant: #43474e;
                --md-sys-color-on-inverse-surface: #f1f0f4;
                --md-sys-color-on-inverse-primary: #003258;
                --md-sys-color-surface-container-lowest: #ffffff;
                --md-sys-color-surface-container-low: #f7f7fa;
                --md-sys-color-surface-container: #f2f2f5;
                --md-sys-color-surface-container-high: #eceef0;
                --md-sys-color-surface-container-highest: #e6e8eb;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Noto Sans JP', sans-serif;
                background-color: var(--md-sys-color-surface-container-low);
                color: var(--md-sys-color-on-surface);
                line-height: 1.6;
                min-height: 100vh;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }
            
            .header {
                background-color: var(--md-sys-color-primary);
                color: var(--md-sys-color-on-primary);
                padding: 2rem 0;
                margin-bottom: 2rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .header h1 {
                text-align: center;
                font-size: 2rem;
                font-weight: 700;
            }
            
            .section {
                background-color: var(--md-sys-color-surface);
                border-radius: 1rem;
                padding: 1.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            
            h2 {
                color: var(--md-sys-color-primary);
                font-size: 1.5rem;
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid var(--md-sys-color-primary-container);
            }
            
            .assignment {
                background-color: var(--md-sys-color-surface);
                border: 1px solid var(--md-sys-color-outline-variant);
                border-radius: 0.75rem;
                padding: 1.25rem;
                margin: 1rem 0;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .assignment:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .assignment::before {
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 4px;
                background-color: var(--md-sys-color-primary);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .assignment:hover::before {
                opacity: 1;
            }
            
            .checkbox {
                appearance: none;
                -webkit-appearance: none;
                width: 1.5rem;
                height: 1.5rem;
                border: 2px solid var(--md-sys-color-outline);
                border-radius: 0.25rem;
                margin-right: 1rem;
                position: relative;
                cursor: pointer;
                vertical-align: middle;
                transition: all 0.2s ease;
            }
            
            .checkbox:checked {
                background-color: var(--md-sys-color-primary);
                border-color: var(--md-sys-color-primary);
            }
            
            .checkbox:checked::after {
                content: '✓';
                position: absolute;
                color: white;
                font-size: 1rem;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
            }
            
            .subject {
                color: var(--md-sys-color-primary);
                font-weight: 700;
                font-size: 1.1rem;
                display: block;
                margin-bottom: 0.5rem;
            }
            
            .title {
                font-size: 1.2rem;
                font-weight: 500;
                margin: 0.5rem 0;
                color: var(--md-sys-color-on-surface);
            }
            
            .category {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                background-color: var(--md-sys-color-secondary-container);
                color: var(--md-sys-color-on-secondary-container);
                border-radius: 1rem;
                font-size: 0.875rem;
                font-weight: 500;
                margin: 0.5rem 0;
            }
            
            .due-date {
                color: var(--md-sys-color-on-surface-variant);
                font-size: 0.875rem;
                margin-top: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .due-date::before {
                content: '⏰';
                font-size: 1rem;
            }
            
            .message {
                background-color: var(--md-sys-color-surface);
                border: 1px solid var(--md-sys-color-outline-variant);
                border-radius: 0.75rem;
                padding: 1.25rem;
                margin: 1rem 0;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .message:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .message.read {
                opacity: 0.7;
                background-color: var(--md-sys-color-surface-container);
            }
            
            .message.unread {
                border-left: 4px solid var(--md-sys-color-primary);
            }
            
            .message-subject {
                color: var(--md-sys-color-primary);
                font-weight: 700;
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
                display: block;
            }
            
            .message-content {
                color: var(--md-sys-color-on-surface);
                font-size: 1rem;
                line-height: 1.6;
                margin-top: 0.5rem;
            }
            
            .message-divider {
                height: 1px;
                background-color: var(--md-sys-color-outline-variant);
                margin: 0.5rem 0;
            }
            
            .urgent {
                border-left: 4px solid var(--md-sys-color-error);
            }
            
            .warning {
                border-left: 4px solid var(--md-sys-color-tertiary);
            }
            
            .assignment.completed {
                opacity: 0.6;
                background-color: var(--md-sys-color-surface-container);
            }
            
            .assignment.completed .title {
                text-decoration: line-through;
            }
            
            .assignment.uncompleted {
                border-left: 4px solid var(--md-sys-color-primary);
            }
            
            @media (max-width: 768px) {
                .container {
                    padding: 1rem;
                }
                
                .header {
                    padding: 1.5rem 0;
                }
                
                .header h1 {
                    font-size: 1.5rem;
                }
                
                .section {
                    padding: 1rem;
                }
                
                .assignment, .message {
                    padding: 1rem;
                }
            }
        </style>
        <script>
            // 課題の状態を保存する関数
            function saveState(assignmentId, isCompleted) {
                const states = JSON.parse(localStorage.getItem('assignment_states') || '{}');
                states[assignmentId] = isCompleted;
                localStorage.setItem('assignment_states', JSON.stringify(states));
                
                const card = document.querySelector(`[data-assignment-id="${assignmentId}"]`);
                if (card) {
                    card.classList.toggle('completed', isCompleted);
                    card.classList.toggle('uncompleted', !isCompleted);
                }
                
                sortAssignments();
            }

            // 課題の状態を復元する関数
            function restoreStates() {
                const states = JSON.parse(localStorage.getItem('assignment_states') || '{}');
                Object.entries(states).forEach(([assignmentId, isCompleted]) => {
                    const card = document.querySelector(`[data-assignment-id="${assignmentId}"]`);
                    if (card) {
                        card.classList.toggle('completed', isCompleted);
                        card.classList.toggle('uncompleted', !isCompleted);
                        const checkbox = card.querySelector('.assignment-checkbox');
                        if (checkbox) {
                            checkbox.checked = isCompleted;
                        }
                    }
                });
                
                sortAssignments();
            }

            // 課題をソートする関数
            function sortAssignments() {
                const container = document.querySelector('.assignments');
                if (!container) return;
                
                const assignments = Array.from(container.children);
                
                assignments.sort((a, b) => {
                    const aCompleted = a.classList.contains('completed');
                    const bCompleted = b.classList.contains('completed');
                    
                    if (aCompleted === bCompleted) {
                        const aDueDate = a.querySelector('.due-date').textContent;
                        const bDueDate = b.querySelector('.due-date').textContent;
                        return aDueDate.localeCompare(bDueDate);
                    }
                    
                    return aCompleted ? 1 : -1;
                });
                
                assignments.forEach(assignment => container.appendChild(assignment));
            }

            // お知らせの未読状態を管理する関数
            function markMessageAsRead(messageId) {
                const readMessages = JSON.parse(localStorage.getItem('read_messages') || '{}');
                readMessages[messageId] = true;
                localStorage.setItem('read_messages', JSON.stringify(readMessages));
                
                const card = document.querySelector(`[data-message-id="${messageId}"]`);
                if (card) {
                    card.classList.add('read');
                }
            }

            // お知らせの状態を復元する関数
            function restoreMessageStates() {
                const readMessages = JSON.parse(localStorage.getItem('read_messages') || '{}');
                document.querySelectorAll('.message').forEach(card => {
                    const messageId = card.getAttribute('data-message-id');
                    if (readMessages[messageId]) {
                        card.classList.add('read');
                    }
                });
            }

            // ページ読み込み時に状態を復元
            document.addEventListener('DOMContentLoaded', function() {
                restoreStates();
                restoreMessageStates();
            });

            // チェックボックスの変更を監視
            document.addEventListener('change', function(e) {
                if (e.target.classList.contains('assignment-checkbox')) {
                    const card = e.target.closest('.assignment');
                    const assignmentId = card.getAttribute('data-assignment-id');
                    saveState(assignmentId, e.target.checked);
                }
            });

            // メッセージのクリックを監視
            document.addEventListener('click', function(e) {
                const messageCard = e.target.closest('.message');
                if (messageCard) {
                    const messageId = messageCard.getAttribute('data-message-id');
                    markMessageAsRead(messageId);
                }
            });
        </script>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <h1>WebClass情報</h1>
            </div>
        </div>
        
        <div class="container">
            <div class="section">
                <h2>課題一覧</h2>
                <div class="assignments">
                    {{ASSIGNMENTS}}
                </div>
            </div>
            
            <div class="section">
                <h2>お知らせ一覧</h2>
                <div class="messages">
                    {{MESSAGES}}
                </div>
            </div>
        </div>
    </body>
    </html>
    """ 