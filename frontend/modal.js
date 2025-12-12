class Modal {
    constructor() {
        this.isOpen = false;
        this.modalElement = null;
    }

    openModal(content) {
        if (!this.modalElement) {
            this.createModalElement();
        }

        const modalContent = this.modalElement.querySelector('.modal-content');
        modalContent.innerHTML = content;

        document.body.appendChild(this.modalElement);
        document.body.style.overflow = 'hidden';
        this.modalElement.style.display = 'flex';
        
        requestAnimationFrame(() => {
            this.modalElement.classList.add('modal-open');
        });

        this.isOpen = true;
    }

    closeModal() {
        if (!this.isOpen || !this.modalElement) return;

        this.modalElement.classList.remove('modal-open');
        
        setTimeout(() => {
            if (this.modalElement && this.modalElement.parentNode) {
                document.body.removeChild(this.modalElement);
            }
            document.body.style.overflow = '';
            this.isOpen = false;
        }, 300);
    }

    createModalElement() {
        this.modalElement = document.createElement('div');
        this.modalElement.className = 'modal-overlay';
        this.modalElement.innerHTML = `
            <div class="modal-container">
                <button class="modal-close">&times;</button>
                <div class="modal-content"></div>
            </div>
        `;

        // Close button handler
        this.modalElement.querySelector('.modal-close').addEventListener('click', () => {
            this.closeModal();
        });

        // Click outside to close
        this.modalElement.addEventListener('click', (e) => {
            if (e.target === this.modalElement) {
                this.closeModal();
            }
        });

        // ESC key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeModal();
            }
        });
    }
}

const modal = new Modal();