<script>
  import { onMount } from 'svelte';
  import Lenis from 'lenis';
  import {
    ArrowUpRight,
    Camera,
    ChevronLeft,
    ChevronRight,
    CircleCheck,
    Globe2,
    Mail,
    MapPin,
    Menu,
    MessageCircle,
    Mic2,
    Music2,
    Phone,
    Play,
    Radio,
    Send,
    Sparkles,
    Users,
    Video,
    X
  } from '@lucide/svelte';
  import LottiePlayer from './lib/LottiePlayer.svelte';
  import { recordSpin, wavePulse } from './lib/lottieAnimations';
  import LoadingScreen from './lib/LoadingScreen.svelte';
  import SvgShader from './lib/SvgShader.svelte';

  const navItems = [
    { href: '#top', label: 'Home' },
    { href: '#create', label: 'Create' },
    { href: '#join', label: 'Join' },
    { href: '#calls', label: 'Calls' },
    { href: '#discover', label: 'Discover' }
  ];

  const partners = [
    'K-Man', 'Lea A.', 'Breeze Lane', 'Samantha Kargbo', 'Daniel Koroma', 'Aminata Cole', 'Cody Fisher', 'Freetown Artists'
  ];

  const featuredWork = [
    {
      client: 'Live Session 01',
      title: 'Aminata K.',
      category: 'Singer-songwriter',
      date: '2026',
      image: '/assets/artist-performance.png',
      summary: 'Live at VYBE Central Session 01.'
    },
    {
      client: 'Artist Profile',
      title: 'Daniel Koroma',
      category: 'Producer',
      date: '2026',
      image: '/assets/studio-room.png',
      summary: 'Producer, audio engineer, and beatmaker.'
    },
    {
      client: 'Live Session 02',
      title: 'Freetown Artists',
      category: 'Collaborative Showcase',
      date: '2026',
      image: '/assets/hero-session.png',
      summary: 'A collective live performance session featuring top rising talent.'
    }
  ];

  const heroWorks = []; // Unused but keeping for syntax safety

  const stats = [
    { num: '150+', label: 'Sessions Completed', icon: Mic2 },
    { num: '40+', label: 'Live Video Cuts', icon: Video },
    { num: '2.3x', label: 'Avg. Artist Growth', icon: Globe2 },
    { num: '98%', label: 'Satisfaction Rate', icon: CircleCheck }
  ];

  const capabilities = [
    {
      num: '01',
      title: 'RECORDING STUDIO',
      desc: 'Music, voice-over, rehearsal, and artist development.',
      bullets: []
    },
    {
      num: '02',
      title: 'LIVE SESSIONS',
      desc: 'Performance content designed for discovery and sharing.',
      bullets: []
    },
    {
      num: '03',
      title: 'CREATIVE COMMUNITY',
      desc: 'A place for producers, storytellers, hosts, and creators to meet.',
      bullets: []
    },
    {
      num: '04',
      title: 'DISCOVER ARTISTS',
      desc: 'Profiles, bios, social links, and performance video for every session artist.',
      bullets: []
    }
  ];

  const processSteps = [
    {
      num: '01',
      title: 'BACKGROUND VOCALISTS',
      desc: 'Open calls for studio vocalists.',
      bullets: []
    },
    {
      num: '02',
      title: 'SESSION MUSICIANS',
      desc: 'Opportunities for instrumentalists.',
      bullets: []
    },
    {
      num: '03',
      title: 'HOSTS',
      desc: 'Looking for charismatic storytellers.',
      bullets: []
    },
    {
      num: '04',
      title: 'PRODUCERS',
      desc: 'Join the production roster.',
      bullets: []
    }
  ];

  const benefits = [
    {
      title: 'Studio',
      desc: 'Professional creation space.'
    },
    {
      title: 'Sessions',
      desc: 'Culturally rooted storytelling.'
    },
    {
      title: 'Platform',
      desc: 'Visibility beyond the session.'
    }
  ];

  const testimonials = [
    {
      quote: 'Vybe Central gave my performance the kind of presence and clean sound I usually only see from high-end international studios.',
      author: 'Samantha Kargbo',
      title: 'Afro-Soul Artist'
    },
    {
      quote: 'The session workflow feels extremely focused. You walk in with a rough draft and walk out with a polished, release-ready record.',
      author: 'Daniel Koroma',
      title: 'Lead Producer'
    },
    {
      quote: 'They understand sound, camera angles, timing, and how to capture the true culture behind an artist rollout.',
      author: 'Aminata Cole',
      title: 'Creative Content Director'
    }
  ];

  const faq = [
    {
      question: 'What services does the studio support?',
      answer: 'The studio is fully equipped for multi-track audio recording, instrument tracking, pre-production rehearsal sessions, cinematic live performance captures, and professional voice over.'
    },
    {
      question: 'What does a talent profile include?',
      answer: 'Every session artist receives a dynamic digital profile featuring high-resolution photography, an editorial bio, quick social links, and the embedded live performance video.'
    },
    {
      question: 'How do I submit to open calls?',
      answer: 'Simply join the community newsletter using the form below. We drop session slots, open calls for session players, background vocalists, and host roles directly to our email/WhatsApp list.'
    }
  ];

  let activeTestimonial = 0;
  let activeFaq = 0;
  let menuOpen = false;
  let isLoading = true;
  let email = '';
  let whatsapp = '';
  let signupState = 'idle';
  let signupMessage = '';

  let activeSlide = 2;
  let freetownTime = '';

  onMount(() => {
    if ('scrollRestoration' in history) {
      history.scrollRestoration = 'manual';
    }
    window.scrollTo(0, 0);

    // Initialize Lenis
    const lenis = new Lenis({
      autoRaf: true,
    });

    // Fallback for native Scroll-Driven Animations
    if (!CSS.supports('(animation-timeline: view()) and (animation-range: entry)')) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view-fallback');
          }
        });
      }, { threshold: 0.15 });

      document.querySelectorAll('.capability-row, .process-step-row, .why-card, .portfolio-card').forEach((el) => {
        observer.observe(el);
      });
    }

    const updateTime = () => {
      const options = {
        timeZone: 'Africa/Freetown',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      };
      const formatter = new Intl.DateTimeFormat('en-US', options);
      try {
        freetownTime = `${formatter.format(new Date())} GMT`;
      } catch (e) {
        const now = new Date();
        const hh = String(now.getUTCHours()).padStart(2, '0');
        const mm = String(now.getUTCMinutes()).padStart(2, '0');
        const ss = String(now.getUTCSeconds()).padStart(2, '0');
        freetownTime = `${hh}:${mm}:${ss} GMT`;
      }
    };
    updateTime();
    const clockInterval = setInterval(updateTime, 1000);

    const testimonialTimer = window.setInterval(() => {
      activeTestimonial = (activeTestimonial + 1) % testimonials.length;
    }, 6000);

    return () => {
      clearInterval(clockInterval);
      window.clearInterval(testimonialTimer);
    };
  });

  function closeMenu() {
    menuOpen = false;
  }

  function submitCommunity() {
    const cleanEmail = email.trim();
    const cleanWhatsApp = whatsapp.trim();
    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleanEmail);
    const phoneOk = cleanWhatsApp.replace(/[^\d+]/g, '').length >= 8;

    if (!emailOk || !phoneOk) {
      signupState = 'error';
      signupMessage = 'Add a valid email and WhatsApp number.';
      return;
    }

    signupState = 'success';
    signupMessage = 'You are on the Vybe Central community list.';
    email = '';
    whatsapp = '';
  }

  const nextTestimonial = () => {
    activeTestimonial = (activeTestimonial + 1) % testimonials.length;
  };

  const previousTestimonial = () => {
    activeTestimonial = (activeTestimonial + testimonials.length - 1) % testimonials.length;
  };
  
  const toggleFaq = (index) => {
    activeFaq = activeFaq === index ? -1 : index;
  };
</script>

<svelte:head>
  <title>Vybe Central® | Creative Studio & Talent Platform</title>
</svelte:head>

{#if isLoading}
  <LoadingScreen on:complete={() => { isLoading = false; window.scrollTo(0, 0); }} />
{/if}

<div class="app-container {isLoading ? 'app-loading' : 'app-ready'}">
  {#if !isLoading}
    <div class="fixed-bg" style="position: fixed; inset: 0; z-index: -1; pointer-events: none;">
      <SvgShader />
    </div>
  {/if}
<main>
<!-- Ora Studio Inspired Hero Section -->
<section class="hero-ora" id="top">
  <!-- Very High Quality SVG Shader Background -->
  {#if !isLoading}
    <SvgShader />
  {/if}

  <!-- Floating Nav Pill -->
  <header class="ora-nav-container">
    <div class="ora-nav-pill">
      <div class="ora-nav-brand">
        <a href="#top" on:click={closeMenu}>
          <img src="/assets/vibe-central-logo.png" alt="Vybe Central" class="nav-logo-img" />
        </a>
      </div>
      <nav class="ora-nav-links">
        <a href="#create" on:click={closeMenu}>CREATE</a>
        <a href="#join" on:click={closeMenu}>JOIN</a>
        <a href="#calls" on:click={closeMenu}>CALLS</a>
        <a href="#discover" on:click={closeMenu}>DISCOVER</a>
      </nav>
      <div class="ora-nav-menu">
        <button class="grid-menu-btn" type="button" aria-label="Menu" on:click={() => (menuOpen = !menuOpen)}>
          <span class="grid-dot"></span><span class="grid-dot"></span>
          <span class="grid-dot"></span><span class="grid-dot"></span>
        </button>
      </div>
    </div>
  </header>

  <!-- Mid-section Content -->
  <div class="ora-main-content">
    <div class="ora-content-left">
      <button class="ora-book-call">
        <span class="btn-text">Studio. Sessions. Community. Discovery.</span>
        <span class="btn-icon">➔</span>
      </button>
      
      <h1 class="ora-headline">
        CREATE.<br/>
        COLLABORATE.<br/>
        BE HEARD.
      </h1>
    </div>

    <div class="ora-content-right">
      <div class="ora-services">
        <div class="services-header">
          <span>WHAT VYBE CENTRAL IS</span>
          <span class="arrow-icon">⤵</span>
        </div>
        <ul class="services-list">
          <li>
            <span class="service-index">&#123;1&#125;</span>
            <span class="service-name">STUDIO</span>
          </li>
          <li>
            <span class="service-index">&#123;2&#125;</span>
            <span class="service-name">SESSIONS</span>
          </li>
          <li>
            <span class="service-index">&#123;3&#125;</span>
            <span class="service-name">PLATFORM</span>
          </li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Giant Bottom Text -->
  <div class="ora-bottom-logo">
    <h1 class="ora-giant-text">
      Vybe<span class="registered">®</span>Central
    </h1>
  </div>
</section>



  <!-- Partner/Artist Marquee -->
  <section class="partners-marquee-section" aria-label="Featured artists marquee">
    <h2 class="partners-title">Trusted by Creative Talents & Creators</h2>
    <div class="partners-scroll-container">
      {#each [...partners, ...partners] as partner}
        <span>{partner} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ── &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      {/each}
    </div>
  </section>

  <!-- Introduction / Manifesto -->
  <section class="section" id="about" aria-labelledby="intro-title">
    <div class="intro-container">
      <div class="intro-label">Brand Overview</div>
      <h2 id="intro-title" class="intro-headline">
        VYBE Central is a creative ecosystem where artists, producers, storytellers, and creators come together to create, collaborate, and be heard.
      </h2>
      <p style="color: var(--text-secondary); max-width: 600px; margin: 2rem auto 0; font-size: 1.1rem; text-align: center;">
        <strong>Mission:</strong> Amplify African voices through studio production, live performance sessions, storytelling, and creative community.<br/><br/>
        <strong>Promise:</strong> Professional creation space, culturally rooted storytelling, and visibility beyond the session.
      </p>
    </div>
  </section>

  <!-- Portfolio (Featured Work) -->
  <section class="section" id="discover" aria-labelledby="work-title">
    <div class="portfolio-header">
      <div class="portfolio-heading">
        <h2 id="work-title">Discover Artists</h2>
        <p>Every performance session becomes a discoverable profile.</p>
      </div>
    </div>

    <div class="portfolio-grid grid-bordered">
      {#each featuredWork as item}
        <article class="portfolio-card">
          <div class="portfolio-img">
            <img src={item.image} alt={item.title} loading="lazy" />
          </div>
          <div class="portfolio-meta">
            <div class="portfolio-category-date">
              <span>{item.category}</span>
              <span>{item.date}</span>
            </div>
            <h3>{item.title}</h3>
            <p class="portfolio-desc">{item.summary}</p>
          </div>
        </article>
      {/each}
    </div>
  </section>

  <!-- Achievements / Stats -->
  <section class="section" aria-labelledby="stats-title">
    <h2 id="stats-title" style="display: none;">Vybe Central Stats</h2>
    <div class="achievements-grid grid-bordered">
      {#each stats as stat}
        <div class="achievement-card">
          <svelte:component this={stat.icon} size={28} />
          <span class="achievement-number">{stat.num}</span>
          <span class="achievement-label">{stat.label}</span>
        </div>
      {/each}
    </div>
  </section>

  <!-- Capabilities (What We Create) -->
  <section class="section" id="create" aria-labelledby="caps-title">
    <div class="portfolio-header">
      <div class="portfolio-heading">
        <h2 id="caps-title">Why Vybe Central?</h2>
        <p>The brand should feel like a working studio and a cultural platform at the same time: precise, cinematic, social, and rooted.</p>
      </div>
    </div>

    <div class="capabilities-list">
      {#each capabilities as cap}
        <article class="capability-row">
          <span class="capability-num">{cap.num}</span>
          <div class="capability-info">
            <h3>{cap.title}</h3>
          </div>
          <div class="capability-details">
            <p>{cap.desc}</p>
          </div>
        </article>
      {/each}
    </div>
  </section>

  <!-- How We Work (Interactive Process) -->
  <section class="section process-section" id="calls" aria-labelledby="process-title">
    <div class="process-header">
      <p class="process-subtitle">Open Calls</p>
      <h2 id="process-title">Community and Open Calls</h2>
      <p style="color: var(--text-secondary); max-width: 600px; margin-top: 1rem; font-size: 1.1rem;">The brand is strongest when people can join, contribute, and see a path into the creative ecosystem.</p>
    </div>

    <div class="process-steps-container">
      {#each processSteps as step}
        <div class="process-step-row">
          <span class="process-step-num">{step.num}</span>
          <h3 class="process-step-title">{step.title}</h3>
          <div class="process-step-content">
            <p>{step.desc}</p>
          </div>
        </div>
      {/each}
    </div>
  </section>

  <!-- Why Choose Us -->
  <section class="section" id="why-us" aria-labelledby="why-title">
    <div class="why-header">
      <h2 id="why-title">Touchpoints</h2>
      <p>The brand needs to work from social cards to studio walls.</p>
    </div>

    <div class="why-grid grid-bordered">
      {#each benefits as benefit}
        <div class="why-card">
          <div class="why-card-icon">
            <Mic2 size={18} />
          </div>
          <h3>{benefit.title}</h3>
          <p>{benefit.desc}</p>
        </div>
      {/each}
    </div>
  </section>

  <!-- Testimonials Carousel -->
  <section class="section" aria-labelledby="test-title">
    <h2 id="test-title" style="display: none;">Artist Feedback</h2>
    <div class="testimonial-box" aria-live="polite">
      <p class="testimonial-label">Stories from Our Partners</p>
      <blockquote class="testimonial-quote">
        “{testimonials[activeTestimonial].quote}”
      </blockquote>
      <p class="testimonial-author">{testimonials[activeTestimonial].author}</p>
      <p class="testimonial-author-title">{testimonials[activeTestimonial].title}</p>
      
      <div class="testimonial-nav-btns">
        <button type="button" class="testimonial-nav-btn" aria-label="Previous testimonial" on:click={previousTestimonial}>
          <ChevronLeft size={18} />
        </button>
        <button type="button" class="testimonial-nav-btn" aria-label="Next testimonial" on:click={nextTestimonial}>
          <ChevronRight size={18} />
        </button>
      </div>
    </div>
  </section>

  <!-- FAQ Section -->
  <section class="section" aria-labelledby="faq-title">
    <div class="faq-container">
      <div class="faq-title-block">
        <h2 id="faq-title">Frequently Asked Questions</h2>
        <p>Quick responses to clarify our services. Got questions? Feel free to reach out!</p>
      </div>
      
      <div class="faq-list">
        {#each faq as item, index}
          <div class="faq-item">
            <button 
              type="button" 
              class="faq-item-btn" 
              aria-expanded={activeFaq === index} 
              on:click={() => toggleFaq(index)}
            >
              <span class="faq-num">[{index + 1}]</span>
              <span class="faq-question">{item.question}</span>
              <span class="faq-toggle-icon">{activeFaq === index ? '−' : '+'}</span>
            </button>
            {#if activeFaq === index}
              <div class="faq-answer-wrapper">
                <p>{item.answer}</p>
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- Reach Out / Signup Form -->
  <section class="section" id="join" aria-labelledby="contact-title">
    <div class="contact-split">
      <div class="contact-info-column">
        <h2 id="contact-title">Join the Ecosystem.</h2>
        <p>Capture email and WhatsApp with a tight community form. Join the list to get open calls directly.</p>
        
        <div class="contact-channels">
          <div class="contact-channel-item">
            <Mail size={18} />
            <a href="mailto:hello@vibecentral.sl">hello@vibecentral.sl</a>
          </div>
          <div class="contact-channel-item">
            <Phone size={18} />
            <a href="tel:+23200000000">+232 00 000 000</a>
          </div>
          <div class="contact-channel-item">
            <MapPin size={18} />
            <span>Freetown, Sierra Leone</span>
          </div>
        </div>
      </div>

      <div class="contact-form-column">
        <h3>Join the Community</h3>
        <p>Receive updates on open calls, session drops, and studio booking promotions.</p>
        
        <form class="contact-form" on:submit|preventDefault={submitCommunity} novalidate>
          <div class="form-group">
            <label for="email-field">Email address</label>
            <input 
              bind:value={email} 
              type="email" 
              id="email-field" 
              class="form-input" 
              placeholder="you@example.com" 
              autocomplete="email" 
              required 
            />
          </div>
          
          <div class="form-group">
            <label for="tel-field">WhatsApp number</label>
            <input 
              bind:value={whatsapp} 
              type="tel" 
              id="tel-field" 
              class="form-input" 
              placeholder="+232 ..." 
              autocomplete="tel" 
              required 
            />
          </div>
          
          <button type="submit" class="form-submit-btn">
            Send Message
            <Send size={16} />
          </button>

          {#if signupMessage}
            <div class="form-status-msg {signupState}">
              {signupMessage}
            </div>
          {/if}
        </form>
      </div>
    </div>
  </section>
</main>

<!-- Footer -->
<footer class="footer-section">
  <div class="footer-top">
    <div class="footer-brand">
      <img src="/assets/vibe-central-logo.png" alt="" />
      <span>Vybe Central</span>
    </div>
    <div class="footer-top-wave">
      <LottiePlayer animationData={recordSpin} ariaLabel="Spinning record animation" />
    </div>
  </div>

  <div class="footer-grid-cols">
    <div>
      <h3 class="footer-col-title">Navigate</h3>
      <div class="footer-col-links">
        {#each navItems as item}
          <a href={item.href}>{item.label}</a>
        {/each}
      </div>
    </div>
    
    <div>
      <h3 class="footer-col-title">Connect</h3>
      <div class="footer-col-links">
        <a href="https://instagram.com/vibecentral" target="_blank" rel="noreferrer">Instagram</a>
        <a href="https://tiktok.com/@vibecentral" target="_blank" rel="noreferrer">TikTok</a>
        <a href="https://youtube.com/@vibecentral" target="_blank" rel="noreferrer">YouTube</a>
        <a href="wa.me/23200000000" target="_blank" rel="noreferrer">WhatsApp</a>
      </div>
    </div>
    
    <div>
      <h3 class="footer-col-title">Legal</h3>
      <div class="footer-col-links">
        <a href="#privacy">Privacy Policy</a>
        <a href="#terms">Terms of Service</a>
        <a href="#gdpr">GDPR Compliance</a>
      </div>
    </div>

    <div class="footer-statement-col">
      <h3 class="footer-col-title">Ecosystem</h3>
      <p class="footer-statement-text">
        Merging design, storytelling, and professional audio technology to make African voices heard globally.
      </p>
      <div class="footer-statement-badge">
        <Sparkles size={16} />
        <span>Built for 2026</span>
      </div>
    </div>
  </div>

  <div class="footer-bottom">
    <p>© 2026 Vybe Central Studio. All rights reserved.</p>
    <p>Created by <a href="https://symche.xyz" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: none;">symche.xyz</a></p>
  </div>
</footer>
</div>

<!-- Mobile Navigation Fullscreen Overlay -->
{#if menuOpen}
  <div class="mobile-nav-overlay" aria-label="Mobile menu">
    <button type="button" class="mobile-nav-close" on:click={closeMenu} aria-label="Close menu">
      <X size={32} />
    </button>
    <nav class="mobile-nav-links">
      {#each navItems as item}
        <a href={item.href} on:click={closeMenu}>{item.label}</a>
      {/each}
    </nav>
  </div>
{/if}
