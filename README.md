# Shamrock Day Spa Website

A modern, responsive spa website inspired by Cloud9 Spa's design aesthetic. This website features a clean, professional layout perfect for day spas, wellness centers, and massage therapy businesses.

## 🌟 Features

- **Responsive Design**: Fully optimized for desktop, tablet, and mobile devices
- **Modern UI/UX**: Clean, elegant design with smooth animations and transitions
- **Easy to Customize**: Well-organized code structure for easy content updates
- **Fast Loading**: Optimized CSS and minimal dependencies
- **Mobile-Friendly Navigation**: Hamburger menu for mobile devices
- **Newsletter Integration**: Built-in newsletter subscription form
- **Service Showcase**: Grid layout for displaying spa services
- **Pricing Section**: Clear pricing presentation with featured packages
- **Contact Information**: Dedicated section for business hours and location

## 🎨 Design

The design follows Cloud9 Spa's aesthetic with:
- Teal and gold color scheme
- Premium typography (Montserrat + Playfair Display)
- Smooth animations and hover effects
- Professional, clean layout

## 📁 Project Structure

```
shamrock-spa-website/
├── index.html          # Main HTML file
├── css/
│   └── styles.css      # All styling
├── js/
│   └── script.js       # JavaScript functionality
├── images/             # Image assets (add your images here)
└── README.md           # This file
```

## 🚀 Getting Started

### Option 1: Open Directly
Simply open `index.html` in your web browser to view the website locally.

### Option 2: Use a Local Server
For better development experience, use a local server:

**Using Python:**
```bash
# Python 3
python -m http.server 8000

# Then visit: http://localhost:8000
```

**Using Node.js (with http-server):**
```bash
npm install -g http-server
http-server

# Then visit: http://localhost:8080
```

**Using VS Code:**
Install the "Live Server" extension and click "Go Live" in the status bar.

## ✏️ Customization Guide

### 1. Update Business Information

Edit `index.html` to update:
- Business name (in header and throughout)
- Services and descriptions
- Pricing information
- Contact details (address, phone, email, hours)
- Social media links

### 2. Customize Colors

Edit `css/styles.css` - modify the CSS variables at the top:

```css
:root {
    --primary-teal: #1B5971;      /* Main brand color */
    --accent-gold: #FBBD48;        /* Accent color */
    /* Customize other colors as needed */
}
```

### 3. Add Images

Place your images in the `images/` folder and update references in `index.html`:
- Add hero background image
- Service images
- Logo image
- Team photos (if applicable)

### 4. Update Content

All content is in `index.html`. Search for and update:
- `<h1>`, `<h2>`, `<h3>` tags for headings
- `<p>` tags for paragraphs
- Service descriptions
- Pricing details
- Hours and location

### 5. Integrate Booking System

The "Book Now" buttons currently show an alert. To integrate a real booking system:

1. **Option A**: Update the booking button links in `index.html`:
   ```html
   <a href="https://your-booking-url.com" class="btn-primary">Book Now</a>
   ```

2. **Option B**: Integrate booking software (Calendly, Square Appointments, etc.)

3. **Option C**: Link to a booking form or modal

## 🔧 Technical Details

### Technologies Used
- HTML5
- CSS3 (with CSS Variables)
- Vanilla JavaScript (no frameworks required)
- Google Fonts (Montserrat, Playfair Display)

### Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

### Performance
- Minimal dependencies
- Optimized CSS
- Lazy loading animations
- Mobile-first responsive design

## 📱 Responsive Breakpoints

- **Desktop**: 1024px and above
- **Tablet**: 768px - 1023px
- **Mobile**: Below 768px
- **Small Mobile**: Below 425px

## 🎯 Features Explanation

### Hero Section
Eye-catching landing section with call-to-action buttons

### Services Grid
Displays all spa services with icons and descriptions

### Pricing Section
Clear pricing with a featured package highlight

### Why Choose Us
Highlights key differentiators and benefits

### Newsletter Signup
Email subscription form with validation

### Mobile Navigation
Responsive hamburger menu for mobile devices

## 🔐 Security Notes

- Newsletter form includes basic email validation
- No sensitive data is stored client-side
- For production: Implement server-side validation and HTTPS

## 📝 To-Do for Production

Before deploying to production:

1. **Add Images**: Replace emoji icons with professional images
2. **Set Up Backend**: Implement newsletter subscription backend
3. **Booking Integration**: Connect to a booking system/API
4. **Analytics**: Add Google Analytics or similar tracking
5. **SEO**:
   - Add meta tags for social sharing
   - Create sitemap.xml
   - Add robots.txt
6. **Contact Form**: Implement a working contact form with backend
7. **SSL Certificate**: Ensure HTTPS is enabled
8. **Performance**: Compress images and minify CSS/JS
9. **Testing**: Test on all devices and browsers

## 📄 License

This template is provided as-is for your use. Feel free to customize and deploy for your business.

## 🤝 Support

For questions or issues with this template:
- Review the code comments in each file
- Check browser console for errors
- Ensure all files are in the correct directory structure

## 🎨 Credits

- Design inspired by Cloud9 Spa
- Built with modern web standards
- Google Fonts for typography

---

**Ready to Launch!** Update the content, add your images, and deploy to your hosting provider.
