let globalUpdateIndicator;
function revealOnScroll() {
    const reveals = document.querySelectorAll('.reveal');
    for (const el of reveals) {
        const windowHeight = window.innerHeight;
        const elementTop = el.getBoundingClientRect().top;
        const revealPoint = 200; 

        if (elementTop < windowHeight - revealPoint) {
            el.classList.add('active');
        } else {
            el.classList.remove('active');
        }
    }
}

window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', revealOnScroll);
document.addEventListener("DOMContentLoaded", function() {
    const navToggle = document.querySelector('.mobile-nav-toggle');
    const nav = document.querySelector('.nav');

    navToggle?.addEventListener('click', () => {
        const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
        navToggle.setAttribute('aria-expanded', !isExpanded);
        nav.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!nav.contains(e.target) && !navToggle.contains(e.target) && nav.classList.contains('active')) {
            nav.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });
    const testimonials = document.querySelectorAll('.testimonial');
  const prevBtn = document.querySelector('.testimonial-btn.prev');
  const nextBtn = document.querySelector('.testimonial-btn.next');
  let current = 0;

  function showTestimonial(idx) {
    testimonials.forEach((t, i) => t.classList.toggle('active', i === idx));
  }

  if (prevBtn && nextBtn) {
    prevBtn.addEventListener('click', function() {
      current = (current - 1 + testimonials.length) % testimonials.length;
      showTestimonial(current);
    });
    nextBtn.addEventListener('click', function() {
      current = (current + 1) % testimonials.length;
      showTestimonial(current);
    });
  }

  // Optionally: swipe gesture support for touch devices
  let startX = null;
  const testimonialSection = document.querySelector('.testimonials');
  if (testimonialSection) {
    testimonialSection.addEventListener('touchstart', function(e) {
      startX = e.touches[0].clientX;
    });
    testimonialSection.addEventListener('touchend', function(e) {
      if (startX === null) return;
      let endX = e.changedTouches[0].clientX;
      if (endX - startX > 40) prevBtn.click();
      else if (startX - endX > 40) nextBtn.click();
      startX = null;
    });
  }
    const steps = document.querySelectorAll(".form-step");
    const nextBtns = document.querySelectorAll(".next-btn");
    const backBtns = document.querySelectorAll(".back-btn");
    const submitBtn = document.querySelector(".submit-button");

    let currentStep = 0;
    steps[currentStep].classList.add("active");

// All RecruitScore JavaScript code //
    const progressContainer = document.createElement("div");
    progressContainer.classList.add("progress-dots");
    steps[0].parentNode.insertBefore(progressContainer, steps[0]);

    steps.forEach((_, i) => {
        const dot = document.createElement("div");
        dot.classList.add("dot");
        if (i === 0) dot.classList.add("active");
        progressContainer.appendChild(dot);
    });

    const dots = document.querySelectorAll(".dot");

    steps.forEach(step => {
        const input = step.querySelector('input, select');
        const nextBtn = step.querySelector('.next-btn');
        
        if (input && nextBtn) {
            input.addEventListener('input', function() {
                if (input.type === 'text' || input.type === 'number') {
                    nextBtn.disabled = !input.value.trim();
                }
                else if (input.tagName === 'SELECT') {
                    nextBtn.disabled = !input.value;
                }
                else if (input.type === 'range') {
                    nextBtn.disabled = false;
                }
            });
        }
    });
    const gpaInput = document.getElementById('GPA');
    if (gpaInput) {
        gpaInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const nextBtn = this.parentElement.querySelector('.next-btn');
            nextBtn.disabled = isNaN(value) || value < 0 || value > 4.0;
        });
    }
    const wpSliders = document.querySelectorAll('.WP-slider');
    wpSliders.forEach(slider => {
        slider.addEventListener('input', function() {
            const valueId = this.id + '-value';
            document.getElementById(valueId).textContent = this.value + '%';
        });
    });
    const feetInput = document.getElementById('player_height-feet');
    const inchesInput = document.getElementById('player_height-inches');

    if (feetInput && inchesInput) {
        feetInput.addEventListener('input', () => validateHeight(feetInput));
        inchesInput.addEventListener('input', () => validateHeight(inchesInput));
    }
    const satInput = document.getElementById('SAT');
    if (satInput) {
    const nextBtn = satInput.parentElement.querySelector('.next-btn');
    // Enable Next on load if SAT is empty
    if (!satInput.value && nextBtn) {
        nextBtn.disabled = false;
    }
    satInput.addEventListener('input', function() {
        const value = parseInt(this.value);
        nextBtn.disabled = !!this.value && (isNaN(value) || value < 400 || value > 1600);
    });
}

    const actInput = document.getElementById('ACT');
    if (actInput) {
        actInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            const nextBtn = this.parentElement.querySelector('.next-btn');
            nextBtn.disabled = !!this.value && (isNaN(value) || value < 12 || value > 36);
        });
    }
    const progressBar = document.querySelector('.progress-dots');
const totalSteps = document.querySelectorAll('.form-step').length;
    function updateProgress() {
    const progress = ((currentStep) / (totalSteps - 1)) * 100;
    progressBar.style.setProperty('--progress', `${progress}%`);
}

    // Handle "Next" button clicks
    nextBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep < steps.length - 1) {
                steps[currentStep].classList.remove("active");
                dots[currentStep].classList.remove("active");
                currentStep++;
                steps[currentStep].classList.add("active");
                dots[currentStep].classList.add("active");
                updateProgress();
            }
        });
    });

    // Handle "Back" button clicks
    backBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentStep > 0) {
                steps[currentStep].classList.remove("active");
                dots[currentStep].classList.remove("active");
                currentStep--;
                steps[currentStep].classList.add("active");
                dots[currentStep].classList.add("active");
                updateProgress();
            }
        });
    });
    const recruitForm = document.getElementById('RSform');
if (recruitForm) {
    recruitForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
        
        // Here you would normally process the form data
        // For now, we'll just redirect to the score page
        window.location.href = 'scorepage.html';
    });
}
});
function validateHeight(input) {
    if (!input.value || isNaN(input.value)) {
        input.value = '';
        return;
    }

    let value = parseInt(input.value);
    const min = parseInt(input.min);
    const max = parseInt(input.max);

    value = Math.max(min, Math.min(max, value));
    
    value = Math.floor(value);
    
    input.value = value;

    const feetInput = document.getElementById('player_height-feet');
    const inchesInput = document.getElementById('player_height-inches');
    const nextBtn = input.closest('.form-step').querySelector('.next-btn');

    const feetValid = feetInput.value && parseInt(feetInput.value) >= 5 && parseInt(feetInput.value) <= 7;
    const inchesValid = inchesInput.value && parseInt(inchesInput.value) >= 0 && parseInt(inchesInput.value) <= 11;
    
    nextBtn.disabled = !(feetValid && inchesValid);
}
// League database //
const stateHSLeagueData = {
    "AL": {
        leagues: ["AHSAA", "AISA"],
        classifications: {
            "AHSAA": ["7A", "6A", "5A", "4A", "3A", "2A", "1A", "No Classification"],
            "AISA": ["SKIP THIS STEP"]
        }
    },
    "AK": {
        leagues: ["ASAA"],
        classifications: {
            "ASAA": ["4A", "3A", "2A", "1A"]
        }
    },
    "AZ": {
        leagues: ["AIA","ACSAA","EYBL Scholastic"],
        classifications: {
            "AIA":["6A", "5A", "4A", "3A", "2A", "1A", "No Classification"],
            "ACSAA":["SKIP THIS STEP"],
            "EYBL Scholastic":["SKIP THIS STEP"]
        }
    },
    "AR": {
        leagues: [],
        classifications: ["6A", "5A", "4A", "3A", "2A", "1A","No Classification"]
    },
    "CA": {
        leagues: ["CIF","EYBL Scholastic","Independent"],
        classifications: {
            "CIF": ["Open Division","Division 1","Division 2","Division 3","Division 4","Division 5"],
            "EYBL Scholastic": ["SKIP THIS STEP"],
            "Independent": ["SKIP THIS STEP"]
        }
    },
    "CO": {
        leagues: ["CHSAA","CCSAA"],
        classifications: {
            "CHSAA": ["5A", "4A", "3A", "2A", "1A", "No Classification"],
            "CCSAA": ["SKIP THIS STEP"]
        }
    },
    "CT": {
        leagues: ["CIAC", "NEPSAC"],
        classifications: {
            "CIAC": ["LL","L","M","S"],
            "NEPSAC": ["AAA","AA","A","B","C",]
        }
    },
    "DE": {
        leagues: [],
        classifications: []
    },
    "DC": {
        leagues: ["DCIAA","WCAC","ISL"],
        classifications: {
            "DCIAA": ["SKIP THIS STEP"],
            "WCAC": ["SKIP THIS STEP"],
            "ISL": ["SKIP THIS STEP"]
        }
    },
    "GA": {
        leagues: ["GHSAA","GISA","GAPPS"],
        classifications: {
            "GHSAA": ["7A", "6A", "5A", "4A", "3A", "2A", "1A"],
            "GISA": ["SKIP THIS STEP"],
            "GAPPS": ["SKIP THIS STEP"]
        }
    },
    "FL": {
        leagues: ["FHSAA","SIAA","EYBL Scholastic"],
        classifications: {
            "FHSAA": ["7A", "6A", "5A", "4A", "3A", "2A", "1A"],
            "SIAA": ["SKIP THIS STEP"],
            "EYBL Scholastic": ["SKIP THIS STEP"]
        }
    },
    "HI": {
        leagues: ["HHSAA","HIA","CSALH"],
        classifications: {
            "HHSAA": ["Division 1","Division 2"],
            "HIA": ["SKIP THIS STEP"],
            "CSALH": ["SKIP THIS STEP"]
        }
    },
    "ID": {
        leagues: ["IHSAA"],
        classifications: ["5A", "4A", "3A", "2A", "1A"]
    },
    "IL": {
        leagues: ["IHSA","CCL","ESCC","ISL(independent)"],
        classifications: {
            "IHSA": ["Class 1A", "Class 2A", "Class 3A", "Class 4A"],
            "CCL": ["SKIP THIS STEP"],
            "ESCC": ["SKIP THIS STEP"],
            "ISL(independent)": ["SKIP THIS STEP"]
        }
    },
    "IN": {
        leagues: ["IHSAA","Independent","EYBL Scholastic"],
        classifications: {
            "IHSAA": ["4A", "3A", "2A", "1A"],
            "Independent": ["SKIP THIS STEP"],
            "EYBL Scholastic": ["SKIP THIS STEP"]
        }
    },
    "IA": {
        leagues: ["IHSAA","ICAC","IISC"],
        classifications: {
            "IHSAA": ["4A", "3A", "2A", "1A"],
            "ICAC": ["SKIP THIS STEP"],
            "IISC": ["SKIP THIS STEP"]
        }
    },
    "KS": {
        leagues: ["KSHSAA","KISAA"],
        classifications: {
            "KSHSAA": ["6A", "5A", "4A", "3A", "2A", "1A"],
            "KISAA": ["SKIP THIS STEP"]
        }
    },
    "KY": {
        leagues: ["KHSAA","Independent"],
        classifications: {
            "KHSAA": ["6A", "5A", "4A", "3A", "2A", "1A"],
            "Independent": ["SKIP THIS STEP"]
        }
    },
    "LA": {
        leagues: ["LHSAA(non-public)","LHSAA(public)"],
        classifications: ["Division 1","Division 2","Division 3","Division 4"]
    },
    "ME": {
        leagues: ["MPA","NEPSAC"],
        classifications: ["AAA","AA","A","B","C","D"]
    },
    "MD": {
        leagues: ["MPSSAA", "WCAC", "MIAA","Independent"],
        classifications: {
            "MPSSAA": ["4A", "3A", "2A", "1A", "No Classification"],
            "WCAC": ["SKIP THIS STEP"],
            "MIAA": ["SKIP THIS STEP"],
            "Independent": ["SKIP THIS STEP"]
        }
    },
    "MA": {
        leagues: ["MIAA", "NEPSAC","EYBL Scholastic"],
        classifications: {
            "MIAA": ["Division 1","Division 2","Division 3","Division 4", "Division 5"],
            "NEPSAC": ["AAA","AA","A","B","C",],
            "EYBL Scholastic": ["SKIP THIS STEP"]
        }
    },
    "MI": {
        leagues: ["MHSAA","CHSL","EYBL Scholastic","Independent(National)","Independent"],
        classifications: {
            "MHSAA": ["A","B","C","D"],
            "CHSL": ["SKIP THIS STEP"],
            "EYBL Scholastic": ["SKIP THIS STEP"],
            "Independent(National)": ["SKIP THIS STEP"],
            "Independent": ["SKIP THIS STEP"]
        }
    },
    "MN": {
        leagues: ["MSHSL","IMAC","MISL"],
        classifications: {
            "MSHSL": ["Class 1A", "Class 2A", "Class 3A", "Class 4A"],
            "IMAC": ["SKIP THIS STEP"],
            "MISL": ["SKIP THIS STEP"]
        }
    },
    "MS": {
        leagues: ["MHSAA","Other"],
        classifications: {
            "MHSAA": ["6A", "5A", "4A", "3A", "2A", "1A", "No Classification"],
            "Other": ["SKIP THIS STEP"]
        }
    },
    "MO": {
        leagues: ["MSHSAA","EYBL Scholastic","MCC","MISAA"],
        classifications: {
            "MSHSAA": ["4A", "3A", "2A", "1A", "No Classification"],
            "EYBL Scholastic": ["SKIP THIS STEP"],
            "MCC": ["SKIP THIS STEP"],
            "MISAA": ["SKIP THIS STEP"]
        }
    },
    "MT": {
        leagues: ["MHSA"],
        classifications: ["AA", "A","B","C"]
    },
    "NE": {
        leagues: ["NSAA","Centennial Conference"],
        classifications: {
            "NSAA": ["A","B","C1","C2","D1","D2"],
            "Centennial Conference": ["SKIP THIS STEP"]
        }
    },
    "NV": {
        leagues: ["NIAA","Other"],
        classifications: {
            "NIAA": ["4A", "3A", "2A", "1A", "No Classification"],
            "Other": ["SKIP THIS STEP"]
        }
    },
    "NH": {
        leagues: ["NHIAA", "NEPSAC","EYBL Scholastic"],
        classifications: {
            "NHIAA": ["Division 1","Division 2","Division 3","Division 4"],
            "NEPSAC": ["AAA","AA","A","B","C",],
            "EYBL Scholastic": ["SKIP THIS STEP"]
        }
    },
    "NJ": {
        leagues: ["NJSIAA","MAPL"],
        classifications: {
            "NJSIAA": ["4","3","2","1", "Non Public A","Non Public B"],
            "MAPL": ["SKIP THIS STEP"]
        }
    },
    "NM": {
        leagues: ["NMAA", "Other"],
        classifications: {
            "NMAA": ["5A", "4A", "3A", "2A", "1A"],
            "Other": ["SKIP THIS STEP"]
        }
    },
    "NY": {
        leagues: ["NYSPHSAA", "PSAL", "CHSAA", "NEPSAC","AIS(Independent)"],
        classifications: {
            "NYSPHSAA": ["AAA", "AA", "A", "B", "C", "D"],
            "PSAL": ["AAA", "AA", "A", "B", "C"],
            "CHSAA": ["AAA", "AA", "A", "B", "C"],
            "NEPSAC": ["AAA", "AA", "A", "B", "C"],
            "AIS(Independent)": [, "AA", "A", "B"]
        }
    },
    "NC": {
        leagues: ["NCHSAA","NCISAA","EYBL Scholastic"],
        classifications: {
            "NCHSAA": ["4A", "3A", "2A", "1A"],
            "NCISAA": ["4A", "3A", "2A", "1A"],
            "EYBL Scholastic": ["SKIP THIS STEP"]
        }
    },
    "ND": {
        leagues: ["NDHSAA"],
        classifications: {
            "NDHSAA": ["Class A", "Class B"]
        }
    },
    "OH": {
        leagues: ["OHSAA","Cleveland Catholic"],
        classifications: {
            "OHSAA": ["Division I", "Division II", "Division III", "Division IV"],
            "Cleveland Catholic": ["SKIP THIS STEP"]
        }
    },
    "OK": {
        leagues: ["OSSAA"],
        classifications: ["6A", "5A", "4A", "3A", "2A", "A", "B"]
    },
    "OR": {
        leagues: ["OSAA","Catholic","Independent"],
        classifications: {
            "OSAA": ["6A", "5A", "4A", "3A", "2A", "1A", "No Classification"],
            "Catholic": ["SKIP THIS STEP"],
            "Independent": ["SKIP THIS STEP"]
        }
    },
    "PA": {
        leagues: ["PIAA","PCL","FSL","MAPL","Inter-Ac"],
        classifications: {
            "PIAA": ["6A", "5A", "4A", "3A", "2A", "1A"],
            "PCL": ["SKIP THIS STEP"],
            "FSL": ["SKIP THIS STEP"],
            "MAPL": ["SKIP THIS STEP"],
            "Inter-Ac": ["SKIP THIS STEP"]
        }
    },
    "RI": {
        leagues: ["RIIL", "NEPSAC"],
        classifications: {
            "RIIL": ["Division 1","Division 2","Division 3"],
            "NEPSAC": ["AAA","AA","A","B","C",]
        }
    },
    "SC": {
        leagues: [],
        classifications: ["5A", "4A", "3A", "2A", "1A", "No Classification"]
    },
    "SD": {
        leagues: ["SDHSAA","SDCSC"],
        classifications: {
            "SDHSAA": ["Class AA","Class A", "Class B"],
            "SDCSC": ["SKIP THIS STEP"]
        }
    },
    "TN": {
        leagues: ["TISAA","DII"],
        classifications: {
            "TISAA": ["4A", "3A", "2A", "1A", "No Classification"],
            "DII": ["AA", "A"]
        }
    },
    "TX": {
        leagues: ["UIL", "TAPPS", "SPC"],
        classifications: {
            "UIL": ["6A", "5A", "4A", "3A", "2A", "1A"],
            "TAPPS": ["6A", "5A", "4A", "3A", "2A", "1A"],
            "SPC": ["SKIP THIS STEP"]
        }
    },
    "UT": {
        leagues: ["UHSAA","Catholic","Independent"],
        classifications: {
            "UHSAA": ["6A", "5A", "4A", "3A", "2A", "1A"],
            "Catholic": ["SKIP THIS STEP"],
            "Independent": ["SKIP THIS STEP"]
        }
    },
    "VT": {
        leagues: ["VPA", "NEPSAC"],
        classifications: {
            "VPA": ["Division 1","Division 2","Division 3","Division 4"],
            "NEPSAC": ["AAA","AA","A","B","C",]
        }
    },
    "VA": {
        leagues: ["VHSL","WCAC","VISAA"],
        classifications: {
            "VHSL": ["6", "5", "4", "3", "2", "1"],
            "WCAC": ["SKIP THIS STEP"],
            "VISAA": ["Division 1","Division 2","Division 3"]
        }
    },
    "WA": {
        leagues: ["WIAA","Catholic","Independent"],
        classifications: {
            "WIAA": ["4A", "3A", "2A", "1A"],
            "Catholic": ["SKIP THIS STEP"],
            "Independent": ["SKIP THIS STEP"]
        }
    },
    "WV": {
        leagues: ["WVSSAC","Independent"],
        classifications: {
            "WVSSAC": ["Class AAA", "Class AA", "Class A"],
            "Independent": ["SKIP THIS STEP"]
        }
    },
    "WI": {
        leagues: ["WIAA","MCC","Trailways","Big East"],
        classifications: {
            "WIAA": ["D1", "D2", "D3", "D4", "D5"],
            "MCC": ["SKIP THIS STEP"],
            "Trailways": ["SKIP THIS STEP"],
            "Big East": ["SKIP THIS STEP"]
        }
    },
    "WY": {
        leagues: ["WSF"],
        classifications: ["4A", "3A", "2A", "1A"]
    }
};
document.addEventListener("DOMContentLoaded", function() {
  const stateSelect = document.getElementById("state");
  const leagueSelect = document.getElementById("HS_league");
  const classificationSelect = document.getElementById("Classification");

  stateSelect.addEventListener("change", () => {
    const state = stateSelect.value;

    leagueSelect.innerHTML = '<option value="">Select a league</option>';
    classificationSelect.innerHTML = '<option value="">Select a classification</option>';

    if (stateHSLeagueData[state]) {
      // If leagues exist, populate league dropdown
      if (stateHSLeagueData[state].leagues && stateHSLeagueData[state].leagues.length > 0) {
        stateHSLeagueData[state].leagues.forEach(league => {
          const option = document.createElement("option");
          option.value = league;
          option.textContent = league;
          leagueSelect.appendChild(option);
        });
        leagueSelect.disabled = false;
        classificationSelect.disabled = true;
      } else {
        // No leagues, just populate classifications if array
        if (Array.isArray(stateHSLeagueData[state].classifications)) {
          stateHSLeagueData[state].classifications.forEach(classif => {
            const option = document.createElement("option");
            option.value = classif;
            option.textContent = classif;
            classificationSelect.appendChild(option);
          });
          classificationSelect.disabled = false;
        }
        leagueSelect.disabled = true;
      }
    }
  });

  leagueSelect.addEventListener("change", () => {
    const state = stateSelect.value;
    const league = leagueSelect.value;
    classificationSelect.innerHTML = '<option value="">Select a classification</option>';

    if (
      stateHSLeagueData[state] &&
      stateHSLeagueData[state].classifications &&
      typeof stateHSLeagueData[state].classifications === "object" &&
      !Array.isArray(stateHSLeagueData[state].classifications) &&
      stateHSLeagueData[state].classifications[league]
    ) {
      stateHSLeagueData[state].classifications[league].forEach(classif => {
        const option = document.createElement("option");
        option.value = classif;
        option.textContent = classif;
        classificationSelect.appendChild(option);
      });
      classificationSelect.disabled = false;
    } else {
      classificationSelect.disabled = true;
    }
  });
});
// All CoachConnect JavaScript code
document.addEventListener('DOMContentLoaded', function() {
  const toggleContainer = document.querySelector('.toggle-menu');
  const buttons = document.querySelectorAll('.toggle-menu button');
  const pages = document.querySelectorAll('.toggle-page');
  
  const indicator = document.createElement('span');
  indicator.className = 'toggle-indicator';
  toggleContainer.appendChild(indicator);
  
  updateIndicator(buttons[0]);
  
  buttons.forEach((btn, index) => {
    btn.addEventListener('click', function() {
      buttons.forEach(b => b.classList.remove('active'));
      pages.forEach(p => p.classList.remove('active'));
      
      btn.classList.add('active');
      const target = btn.getAttribute('data-target');
      document.getElementById(target).classList.add('active');
      
      updateIndicator(btn);
    });
  });
  
  function updateIndicator(activeButton) {
    const buttonWidth = activeButton.offsetWidth;
    const buttonLeft = activeButton.offsetLeft;
    
    indicator.style.width = `${buttonWidth}px`;
    indicator.style.transform = `translateX(${buttonLeft}px)`;
  }
  
  if (buttons.length && pages.length) {
    buttons[0].classList.add('active');
    pages[0].classList.add('active');
    updateIndicator(buttons[0]);
  }

document.querySelectorAll('.conference-item a[data-target-page]').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    const pageId = this.getAttribute('data-target-page');
    const targetId = this.getAttribute('href').replace('#', '');
    
    buttons.forEach(b => b.classList.remove('active'));
    pages.forEach(p => p.classList.remove('active'));
    
    const targetButton = document.querySelector(`.toggle-menu button[data-target="${pageId}"]`);
    if (targetButton) {
      targetButton.classList.add('active');
      updateIndicator(targetButton);
    }
    
    document.getElementById(pageId).classList.add('active');
    
    setTimeout(() => {
      const target = document.getElementById(targetId);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  });
});
function initBackToTop() {
    const backToTopButton = document.getElementById('back-to-top');
    const header = document.getElementById('header');
    const toggleMenu = document.querySelector('.toggle-menu');
    
    if (!backToTopButton || !header || !toggleMenu) return;
    
    function toggleBackToTopVisibility() {
      const headerBottom = header.offsetTop + header.offsetHeight;
      const menuBottom = toggleMenu.offsetTop + toggleMenu.offsetHeight;
      const threshold = Math.max(headerBottom, menuBottom);
      
      if (window.scrollY > threshold) {
        backToTopButton.classList.add('visible');
      } else {
        backToTopButton.classList.remove('visible');
      }
    }
    
    backToTopButton.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
    
    window.addEventListener('scroll', toggleBackToTopVisibility);
    toggleBackToTopVisibility();
  }
  initBackToTop();
  const style = document.createElement('style');
  style.textContent = `
    .college-item.highlight {
      background-color: rgba(123, 175, 212, 0.3);
      border-radius: 4px;
      padding: 5px;
      transition: background-color 0.5s ease;
    }
    .school-suggestions li {
      padding: 12px 20px;
      cursor: pointer;
      transition: background 0.2s;
    }
    .school-suggestions li:hover {
      background: #f0f7ff;
    }
  `;
  document.head.appendChild(style);
});
function filterColleges() {
  const searchInput = document.getElementById('school-search-bar');
  const searchTerm = searchInput.value.toLowerCase().trim();
  const suggestionsList = document.getElementById('school-suggestions');
  
  suggestionsList.innerHTML = '';
  
  if (searchTerm.length < 2) {
    suggestionsList.style.display = 'none';
    return;
  }
  
  const colleges = document.querySelectorAll('.college-item a');
  const matchingColleges = [];
  
  colleges.forEach(college => {
    const collegeName = college.textContent.toLowerCase();
    if (collegeName.includes(searchTerm)) {
      const togglePage = college.closest('.toggle-page');
      matchingColleges.push({
        name: college.textContent,
        element: college.parentElement,
        pageId: togglePage ? togglePage.id : null
      });
    }
  });
  
  if (matchingColleges.length > 0) {
    suggestionsList.style.display = 'block';
    
    matchingColleges.slice(0, 8).forEach(college => {
      const li = document.createElement('li');
      li.textContent = college.name;
      li.style.color = '#333';
      
      li.addEventListener('click', () => {
        const pages = document.querySelectorAll('.toggle-page');
        const buttons = document.querySelectorAll('.toggle-menu button');
        
        if (college.pageId) {
          pages.forEach(p => p.classList.remove('active'));
          document.getElementById(college.pageId).classList.add('active');
          
          const targetButton = document.querySelector(`.toggle-menu button[data-target="${college.pageId}"]`);
          if (targetButton) {
            buttons.forEach(b => b.classList.remove('active'));
            targetButton.classList.add('active');
            
            if (typeof updateIndicator === 'function') {
              updateIndicator(targetButton);
            } else if (typeof globalUpdateIndicator === 'function') {
              globalUpdateIndicator(targetButton);
            }
          }
        }
        
        setTimeout(() => {
          college.element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          
          college.element.classList.add('highlight');
          setTimeout(() => {
            college.element.classList.remove('highlight');
          }, 2000);
        }, 100);
        
        searchInput.value = '';
        suggestionsList.style.display = 'none';
      });
      
      suggestionsList.appendChild(li);
    });
  } else {
    const li = document.createElement('li');
    li.textContent = 'No matches found';
    li.style.color = '#666';
    li.style.fontStyle = 'italic';
    suggestionsList.appendChild(li);
    suggestionsList.style.display = 'block';
  }
}

document.addEventListener('click', function(e) {
  const searchBar = document.getElementById('school-search-bar');
  const suggestions = document.getElementById('school-suggestions');
  
  if (e.target !== searchBar && (!suggestions || !suggestions.contains(e.target))) {
    if (suggestions) {
      suggestions.style.display = 'none';
    }
  }
});
