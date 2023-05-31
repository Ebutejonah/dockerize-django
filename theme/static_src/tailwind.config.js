/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        
        '../../core/templates/*.html', '../../core/templates/partials/*.html', '../../core/templates/registration/*.html', '../../core/static/main.js',
        
    ],
    prefix : "tw-",
    important: true,
    theme: {
        extend: {},
    },
    darkMode : 'class',
    corePlugins:{
        preflight: false,
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
