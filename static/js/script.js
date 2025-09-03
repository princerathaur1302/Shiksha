// JavaScript for Siksha Academy

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault()
            
            const targetId = this.getAttribute('href')
            if (targetId === '#') return
            
            const targetElement = document.querySelector(targetId)
            if (targetElement) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                })
                
                // Update URL
                if (history.pushState) {
                    history.pushState(null, null, targetId)
                } else {
                    location.hash = targetId
                }
            }
        })
    })

    // Form validation
    const forms = document.querySelectorAll('.needs-validation')
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            
            form.classList.add('was-validated')
        }, false)
    })

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert')
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert)
            bsAlert.close()
        }, 5000)
    })

    // Back to top button
    const backToTopButton = document.createElement('button')
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>'
    backToTopButton.classList.add('btn', 'btn-primary', 'btn-lg', 'back-to-top')
    backToTopButton.style.position = 'fixed'
    backToTopButton.style.bottom = '20px'
    backToTopButton.style.right = '20px'
    backToTopButton.style.zIndex = '1000'
    backToTopButton.style.display = 'none'
    backToTopButton.style.borderRadius = '50%'
    backToTopButton.style.width = '50px'
    backToTopButton.style.height = '50px'
    backToTopButton.style.padding = '0'
    document.body.appendChild(backToTopButton)

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' })
    })

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block'
        } else {
            backToTopButton.style.display = 'none'
        }
    })

    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]')
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target
                    img.src = img.dataset.src
                    img.removeAttribute('data-src')
                    imageObserver.unobserve(img)
                }
            })
        })
        
        lazyImages.forEach(img => {
            imageObserver.observe(img)
        })
    }
})

// Additional functions for admin/teacher dashboards
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?')
}

function showLoading() {
    const loadingElement = document.createElement('div')
    loadingElement.id = 'loading-overlay'
    loadingElement.style.position = 'fixed'
    loadingElement.style.top = '0'
    loadingElement.style.left = '0'
    loadingElement.style.width = '100%'
    loadingElement.style.height = '100%'
    loadingElement.style.backgroundColor = 'rgba(255, 255, 255, 0.8)'
    loadingElement.style.display = 'flex'
    loadingElement.style.justifyContent = 'center'
    loadingElement.style.alignItems = 'center'
    loadingElement.style.zIndex = '9999'
    
    const spinner = document.createElement('div')
    spinner.classList.add('spinner-border', 'text-primary')
    spinner.style.width = '3rem'
    spinner.style.height = '3rem'
    
    loadingElement.appendChild(spinner)
    document.body.appendChild(loadingElement)
    
    return () => {
        document.body.removeChild(loadingElement)
    }
}