/* ==========================================
   BLOG PAGE - DYNAMIC CONTENT LOADING
   ========================================== */

// NEWS API Configuration
const NEWS_API_KEY = '0c3fa8f5ac3046ad868d6bf6cf7da873'; // Đăng ký miễn phí tại https://newsapi.org
const BLOG_API_URL = 'https://newsapi.org/v2/everything';

// Category mapping với keywords cụ thể hơn
const CATEGORIES = {
    all: 'organic food OR healthy eating OR sustainable food',
    recipes: 'organic recipes OR healthy recipes OR cooking',
    health: 'organic food health benefits OR nutrition',
    gardening: 'organic gardening OR urban farming OR grow vegetables',
    sustainability: 'sustainable food OR eco-friendly eating OR zero waste'
};

// Category colors cho badge
const CATEGORY_COLORS = {
    recipes: '#FFE600',      // Yellow
    health: '#FF69B4',       // Pink
    gardening: '#4CAF50',    // Green
    sustainability: '#3498DB', // Blue
    all: '#FF6B35'          // Orange
};

let currentCategory = 'all';
let currentPage = 1;
const articlesPerPage = 9;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadArticles(currentCategory);
    setupCategoryFilter();
    setupLoadMore();
});

// Load Articles from API
async function loadArticles(category, page = 1) {
    const blogGrid = document.getElementById('blog-grid');
    blogGrid.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading fresh articles...</p>
        </div>
    `;

    try {
        const query = CATEGORIES[category];
        const response = await fetch(
            `${BLOG_API_URL}?q=${encodeURIComponent(query)}&language=en&sortBy=publishedAt&pageSize=${articlesPerPage}&page=${page}&apiKey=${NEWS_API_KEY}`
        );

        if (!response.ok) throw new Error('Failed to fetch articles');

        const data = await response.json();

        // Gán category cho mỗi article
        const articlesWithCategory = data.articles.map(article => ({
            ...article,
            category: category === 'all' ? getCategoryFromContent(article) : category
        }));

        displayArticles(articlesWithCategory);

    } catch (error) {
        console.error('Error loading articles:', error);
        displaySampleArticles(category);
    }
}

// Display Articles
function displayArticles(articles) {
    const blogGrid = document.getElementById('blog-grid');
    blogGrid.innerHTML = '';

    if (articles.length === 0) {
        blogGrid.innerHTML = `
            <div class="no-articles" style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
                <h3 style="font-size: 2rem; margin-bottom: 16px;">🌿 No articles found</h3>
                <p>Try selecting a different category</p>
            </div>
        `;
        return;
    }

    articles.forEach((article, index) => {
        const card = createBlogCard(article, index);
        blogGrid.appendChild(card);
    });
}

// Create Blog Card
function createBlogCard(article, index) {
    const card = document.createElement('article');
    card.className = 'blog-card';

    const category = article.category || 'health';
    const categoryDisplay = category.charAt(0).toUpperCase() + category.slice(1);
    const readTime = calculateReadTime(article.description || article.content || '');
    const publishDate = formatDate(article.publishedAt);

    // Xử lý ảnh: ưu tiên ảnh từ API, fallback sang placeholder
    const imageUrl = getValidImageUrl(article.urlToImage);

    card.innerHTML = `
        <div class="blog-card-image">
        <img src="${imageUrl}" 
            alt="${escapeHtml(article.title)}"
            onerror="this.src='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80'">
        <span class="blog-category-badge" style="background: ${CATEGORY_COLORS[category]}">
            ${categoryDisplay}
        </span>
    </div>
   
    <div class="blog-card-content">
         <br><br>
        <h3 class="blog-card-title">${truncateText(article.title, 70)}</h3>
        <p class="blog-card-excerpt">
            ${truncateText(article.description || 'Discover more about this topic...', 140)}
        </p>

        <div class="blog-card-meta">
            <span><i class="lni lni-calendar"></i> ${publishDate}</span>
            <span><i class="lni lni-timer"></i> ${readTime} min read</span>
        </div>

        <br><br>

        <div class="blog-card-footer">
            <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="read-more-btn">
                Read Article <i class="lni lni-arrow-right"></i>
            </a>
        </div>
    </div>

    `;

    return card;
}

// ==================== HELPER FUNCTIONS ====================

// Xác định category dựa trên nội dung (cho trường hợp "all")
function getCategoryFromContent(article) {
    const text = (article.title + ' ' + article.description).toLowerCase();

    const keywords = {
        recipes: ['recipe', 'cook', 'dish', 'meal', 'ingredient', 'prepare'],
        gardening: ['garden', 'grow', 'plant', 'farming', 'harvest', 'soil'],
        sustainability: ['sustainable', 'eco', 'environment', 'zero waste', 'climate'],
        health: ['health', 'nutrition', 'benefit', 'wellness', 'vitamin']
    };

    let maxScore = 0;
    let detectedCategory = 'health'; // default

    for (const [category, words] of Object.entries(keywords)) {
        const score = words.filter(word => text.includes(word)).length;
        if (score > maxScore) {
            maxScore = score;
            detectedCategory = category;
        }
    }

    return detectedCategory;
}

// Xác thực và lấy URL ảnh hợp lệ
function getValidImageUrl(url) {
    // Nếu không có URL hoặc URL không hợp lệ
    if (!url || url === 'null' || url === 'undefined') {
        return getPlaceholderImage(currentCategory);
    }

    // Kiểm tra URL có phải từ nguồn tin cậy
    try {
        const urlObj = new URL(url);
        // Một số domain hay bị lỗi CORS
        const blockedDomains = ['localhost', '127.0.0.1'];
        if (blockedDomains.some(domain => urlObj.hostname.includes(domain))) {
            return getPlaceholderImage(currentCategory);
        }
        return url;
    } catch {
        return getPlaceholderImage(currentCategory);
    }
}

// Lấy ảnh placeholder phù hợp với category
function getPlaceholderImage(category) {
    const placeholders = {
        recipes: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80', // Salad
        health: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=80', // Healthy food
        gardening: 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&q=80', // Garden
        sustainability: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800&q=80', // Eco
        all: 'https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=800&q=80' // Organic food
    };

    return placeholders[category] || placeholders.all;
}

function calculateReadTime(text) {
    const wordsPerMinute = 200;
    const words = text ? text.split(/\s+/).length : 300;
    return Math.max(5, Math.min(15, Math.ceil(words / wordsPerMinute)));
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;

    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength).trim() + '...';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== EVENT HANDLERS ====================

function setupCategoryFilter() {
    const categoryButtons = document.querySelectorAll('.category-pill');

    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const newCategory = button.dataset.category;
            if (newCategory !== currentCategory) {
                currentCategory = newCategory;
                currentPage = 1;
                loadArticles(currentCategory, currentPage);
            }
        });
    });
}

function setupLoadMore() {
    const loadMoreBtn = document.getElementById('load-more');

    loadMoreBtn.addEventListener('click', async () => {
        loadMoreBtn.textContent = 'Loading...';
        loadMoreBtn.disabled = true;

        try {
            currentPage++;
            const query = CATEGORIES[currentCategory];
            const response = await fetch(
                `${BLOG_API_URL}?q=${encodeURIComponent(query)}&language=en&sortBy=publishedAt&pageSize=${articlesPerPage}&page=${currentPage}&apiKey=${NEWS_API_KEY}`
            );

            const data = await response.json();
            const blogGrid = document.getElementById('blog-grid');

            const articlesWithCategory = data.articles.map(article => ({
                ...article,
                category: currentCategory === 'all' ? getCategoryFromContent(article) : currentCategory
            }));

            articlesWithCategory.forEach((article, index) => {
                const card = createBlogCard(article, index);
                blogGrid.appendChild(card);
            });

        } catch (error) {
            console.error('Error loading more articles:', error);
        } finally {
            loadMoreBtn.textContent = 'Load More Articles';
            loadMoreBtn.disabled = false;
        }
    });
}

// ==================== FALLBACK DATA ====================

function displaySampleArticles(category = 'all') {
    const sampleData = {
        recipes: [
            {
                title: "Fall Harvest: 10 Delicious Seasonal Recipes",
                description: "Make the most of autumn's bounty with these nutritious and delicious organic recipes for the whole family.",
                urlToImage: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80",
                publishedAt: "2023-09-28T10:00:00Z",
                url: "#",
                category: "recipes"
            },
            {
                title: "Quick & Easy Organic Breakfast Ideas",
                description: "Start your day right with these simple, healthy breakfast recipes using fresh organic ingredients.",
                urlToImage: "https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?w=800&q=80",
                publishedAt: "2023-09-25T08:00:00Z",
                url: "#",
                category: "recipes"
            },
            {
                title: "Plant-Based Power Bowls for Every Season",
                description: "Discover how to create balanced, nutrient-packed bowls with organic vegetables and grains.",
                urlToImage: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80",
                publishedAt: "2023-09-20T12:00:00Z",
                url: "#",
                category: "recipes"
            }
        ],
        health: [
            {
                title: "5 Surprising Benefits of Eating Organic",
                description: "Beyond just avoiding pesticides, organic foods offer numerous health benefits that might surprise you.",
                urlToImage: "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=80",
                publishedAt: "2023-10-10T10:00:00Z",
                url: "#",
                category: "health"
            },
            {
                title: "The Science Behind Organic Nutrition",
                description: "Research shows organic produce contains higher levels of antioxidants and beneficial nutrients.",
                urlToImage: "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800&q=80",
                publishedAt: "2023-10-05T09:00:00Z",
                url: "#",
                category: "health"
            },
            {
                title: "How Organic Food Supports Your Immune System",
                description: "Learn how choosing organic can boost your body's natural defenses and improve overall wellness.",
                urlToImage: "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=800&q=80",
                publishedAt: "2023-09-30T11:00:00Z",
                url: "#",
                category: "health"
            }
        ],
        gardening: [
            {
                title: "Start Your Urban Organic Garden Today",
                description: "Limited space is no excuse! Learn how to grow organic vegetables in your apartment or small yard.",
                urlToImage: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&q=80",
                publishedAt: "2023-10-05T14:00:00Z",
                url: "#",
                category: "gardening"
            },
            {
                title: "Composting 101: Turn Waste into Garden Gold",
                description: "Master the art of composting to create nutrient-rich soil for your organic garden.",
                urlToImage: "https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=800&q=80",
                publishedAt: "2023-09-28T13:00:00Z",
                url: "#",
                category: "gardening"
            },
            {
                title: "Seasonal Planting Guide for Organic Gardens",
                description: "Know what to plant and when for a thriving organic garden all year round.",
                urlToImage: "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=800&q=80",
                publishedAt: "2023-09-22T10:00:00Z",
                url: "#",
                category: "gardening"
            }
        ],
        sustainability: [
            {
                title: "Zero Waste Kitchen: Practical Tips",
                description: "Reduce your environmental impact with these simple strategies for a more sustainable kitchen.",
                urlToImage: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800&q=80",
                publishedAt: "2023-10-08T15:00:00Z",
                url: "#",
                category: "sustainability"
            },
            {
                title: "The True Cost of Non-Organic Farming",
                description: "Understanding the environmental impact of conventional agriculture and why organic matters.",
                urlToImage: "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&q=80",
                publishedAt: "2023-10-01T12:00:00Z",
                url: "#",
                category: "sustainability"
            },
            {
                title: "Sustainable Living: Small Changes, Big Impact",
                description: "Easy lifestyle adjustments that make a real difference for our planet's future.",
                urlToImage: "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800&q=80",
                publishedAt: "2023-09-25T16:00:00Z",
                url: "#",
                category: "sustainability"
            }
        ]
    };

    const articles = category === 'all'
        ? [...sampleData.recipes, ...sampleData.health, ...sampleData.gardening].slice(0, 9)
        : sampleData[category] || sampleData.health;

    displayArticles(articles);
}