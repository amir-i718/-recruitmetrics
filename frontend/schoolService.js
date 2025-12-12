class SchoolService {
    constructor() {
        this.cache = new Map();
        this.API_BASE_URL = 'http://localhost:8040'; // FastAPI server
    }

    async getSchoolById(id) {
        if (this.cache.has(id)) {
            return this.cache.get(id);
        }

        try {
            const response = await fetch(`${this.API_BASE_URL}/schools/${id}`);
            
            if (!response.ok) {
                throw new Error(response.status === 404 ? 'School not found' : 'Failed to fetch school data');
            }

            const schoolData = await response.json();
            this.cache.set(id, schoolData);
            return schoolData;
        } catch (error) {
            console.error('Error fetching school:', error);
            throw error;
        }
    }
}

const schoolService = new SchoolService();