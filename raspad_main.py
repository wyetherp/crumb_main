#!/usr/bin/env python3
"""
🌀 Crumb UI - Minimal Sacred Interface v0.2 
Clean, magical, reliable interface for RasPad touchscreen
Designed with sacred intention and mystical beauty
"""

import tkinter as tk
from tkinter import font
import sys
import traceback
import pygame
import os
from datetime import datetime

class CrumbUI:
    def __init__(self):
        try:
            # Initialize the sacred vessel
            self.root = tk.Tk()
            self.root.title("✧ Crumb ✧")
            self.root.configure(bg='#1a1a2e')
            
            # Configure for RasPad touchscreen
            self.root.geometry("1024x600")
            self.root.attributes('-fullscreen', True)
            
            # Sacred color palette
            self.colors = {
                'void': '#0f0f23',
                'deep': '#1a1a2e', 
                'mystic': '#16213e',
                'ethereal': '#e94560',
                'gold': '#f3a712',
                'sage': '#53a8b6',
                'earth': '#8b5a3c',
                'fire': '#ff6b35',
                'water': '#4ecdc4',
                'air': '#95e1d3',
                'aether': '#c44569'
            }
            
            # Initialize state
            self.current_screen = "hub"
            self.exit_taps = 0
            self.animation_running = False
            
            # Setup systems
            self.setup_fonts()
            self.setup_audio()
            
            # Create main container
            self.main_frame = tk.Frame(self.root, bg=self.colors['deep'])
            self.main_frame.pack(fill='both', expand=True)
            
            # Create screens
            self.screens = {}
            self.create_hub_screen()
            self.create_placeholder_screens()
            
            # Start hub
            self.show_screen('hub')
            
            # Play startup music
            self.play_startup_music()
            
            # Setup interactions
            self.root.bind('<Button-1>', self.handle_click)
            
            # Start animations
            self.start_animations()
            
            print("✧ Crumb UI v0.2 initialized successfully ✧")
            
        except Exception as e:
            self.handle_error("Initialization", e)

    def setup_fonts(self):
        """Initialize sacred typography"""
        try:
            self.fonts = {
                'title': font.Font(family="Arial", size=28, weight="bold"),
                'subtitle': font.Font(family="Arial", size=14),
                'body': font.Font(family="Arial", size=12),
                'button': font.Font(family="Arial", size=16, weight="bold"),
                'large_symbol': font.Font(family="Arial", size=32, weight="bold"),
                'companion': font.Font(family="Arial", size=24)
            }
        except Exception as e:
            print(f"Font setup warning: {e}")
            # Fallback fonts
            self.fonts = {
                'title': ('Arial', 28, 'bold'),
                'subtitle': ('Arial', 14),
                'body': ('Arial', 12),
                'button': ('Arial', 16, 'bold'),
                'large_symbol': ('Arial', 32, 'bold'),
                'companion': ('Arial', 24)
            }

    def setup_audio(self):
        """Initialize audio system"""
        try:
            # Try USB speaker first
            os.environ['SDL_AUDIODRIVER'] = 'alsa'
            os.environ['ALSA_PCM_DEVICE'] = '2'
            
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            self.audio_enabled = True
            print("✧ Audio system initialized ✧")
        except Exception as e:
            print(f"Audio initialization error: {e}")
            try:
                pygame.mixer.init()
                self.audio_enabled = True
                print("✧ Audio system initialized with default device ✧")
            except:
                self.audio_enabled = False
                print("✧ Audio disabled ✧")

    def play_startup_music(self):
        """Play continuous background music"""
        if not self.audio_enabled:
            return
        try:
            startup_file = "/home/pi/Downloads/startup.mp3"
            if os.path.exists(startup_file):
                pygame.mixer.music.load(startup_file)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)  # Loop forever
                print("✧ Startup music playing ✧")
        except Exception as e:
            print(f"Music error: {e}")

    def create_hub_screen(self):
        """🏠 The Sacred Hub - Enhanced with magic"""
        hub = tk.Frame(self.main_frame, bg=self.colors['deep'])
        
        # Main content container
        content_frame = tk.Frame(hub, bg=self.colors['deep'])
        content_frame.pack(expand=True)
        
        # Title section with enhanced styling
        title_frame = tk.Frame(content_frame, bg=self.colors['deep'])
        title_frame.pack(pady=(50, 30))
        
        # Main title with glow effect
        main_title = tk.Label(title_frame, 
                             text="✧ CRUMB ✧", 
                             font=self.fonts['title'],
                             fg=self.colors['gold'],
                             bg=self.colors['deep'])
        main_title.pack()
        
        # Glowing subtitle
        subtitle = tk.Label(title_frame, 
                           text="A Friendly AI for Real-Life Support", 
                           font=self.fonts['subtitle'],
                           fg=self.colors['sage'],
                           bg=self.colors['deep'])
        subtitle.pack(pady=(10, 0))
        
        # Sacred tagline
        tagline = tk.Label(title_frame, 
                          text="✦ Sacred Companion • Testing Interface ✦", 
                          font=self.fonts['body'],
                          fg=self.colors['aether'],
                          bg=self.colors['deep'])
        tagline.pack(pady=(5, 0))
        
        # Companion and navigation area
        nav_container = tk.Frame(content_frame, bg=self.colors['deep'])
        nav_container.pack(expand=True)
        
        # Left side - Floating companion
        companion_frame = tk.Frame(nav_container, bg=self.colors['deep'])
        companion_frame.pack(side='left', fill='y', padx=(80, 40))
        
        # Animated companion - will be animated later
        self.companion = tk.Label(companion_frame, 
                                 text="🌟", 
                                 font=self.fonts['companion'],
                                 fg=self.colors['gold'],
                                 bg=self.colors['deep'])
        self.companion.pack(expand=True)
        
        companion_msg = tk.Label(companion_frame, 
                                text="Hello,\nfriend!", 
                                font=self.fonts['body'],
                                fg=self.colors['water'],
                                bg=self.colors['deep'],
                                justify='center')
        companion_msg.pack()
        
        # Right side - Navigation buttons
        nav_frame = tk.Frame(nav_container, bg=self.colors['deep'])
        nav_frame.pack(side='right', padx=(40, 80))
        
        # Sacred navigation buttons in 2x2 grid
        buttons = [
            ("🌍", "Elements", self.colors['earth'], 'elemental'),
            ("🎵", "Sounds", self.colors['ethereal'], 'soundboard'),
            ("🧙‍♂️", "Archetypes", self.colors['aether'], 'archetype'),
            ("⚙️", "Settings", self.colors['mystic'], 'settings')
        ]
        
        for i, (symbol, label, color, screen) in enumerate(buttons):
            row, col = i // 2, i % 2
            
            btn = tk.Button(nav_frame,
                           text=f"{symbol}\n{label}",
                           font=self.fonts['button'],
                           fg='white',
                           bg=color,
                           activebackground=self.lighten_color(color),
                           activeforeground='white',
                           bd=0,
                           relief='flat',
                           width=9,
                           height=3,
                           command=lambda s=screen: self.safe_navigate(s))
            btn.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Configure grid weights for responsive layout
        nav_frame.grid_rowconfigure(0, weight=1)
        nav_frame.grid_rowconfigure(1, weight=1)
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)
        
        # Sparkle background elements
        self.create_sparkles(hub)
        
        self.screens['hub'] = hub

    def create_sparkles(self, parent):
        """Add subtle sparkle background"""
        try:
            sparkle_positions = [(150, 120), (850, 180), (200, 450), (800, 380), (500, 100)]
            self.sparkles = []
            
            for x, y in sparkle_positions:
                sparkle = tk.Label(parent, 
                                  text="✦", 
                                  font=('Arial', 8),
                                  fg=self.colors['sage'],
                                  bg=self.colors['deep'])
                sparkle.place(x=x, y=y)
                self.sparkles.append(sparkle)
        except Exception as e:
            print(f"Sparkle creation error: {e}")

    def create_placeholder_screens(self):
        """Create simplified placeholder screens"""
        screens_config = [
            ('elemental', "✧ Elemental Modes ✧", "🌱", "Sacred elemental forces await..."),
            ('soundboard', "✧ Sacred Sounds ✧", "🎵", "Expression tools in development..."),
            ('archetype', "✧ Archetype Portal ✧", "🧙‍♂️", "Mystical companions awakening..."),
            ('settings', "✧ Sacred Settings ✧", "⚙️", "Configuration options coming soon...")
        ]
        
        for screen_name, title, symbol, message in screens_config:
            try:
                self.create_placeholder_screen(screen_name, title, symbol, message)
            except Exception as e:
                print(f"Error creating {screen_name}: {e}")

    def create_placeholder_screen(self, name, title, symbol, message):
        """Create a clean placeholder screen"""
        screen = tk.Frame(self.main_frame, bg=self.colors['void'])
        
        # Header with back button
        header = tk.Frame(screen, bg=self.colors['void'])
        header.pack(fill='x', pady=30)
        
        # Back button
        back_btn = tk.Button(header, 
                            text="← Back to Hub",
                            font=self.fonts['body'],
                            fg=self.colors['sage'],
                            bg=self.colors['deep'],
                            activebackground=self.lighten_color(self.colors['deep']),
                            bd=0,
                            padx=20,
                            pady=10,
                            command=lambda: self.safe_navigate('hub'))
        back_btn.pack(side='left', padx=30)
        
        # Title
        title_label = tk.Label(header, 
                              text=title,
                              font=self.fonts['title'],
                              fg=self.colors['gold'],
                              bg=self.colors['void'])
        title_label.pack()
        
        # Content area
        content_frame = tk.Frame(screen, bg=self.colors['void'])
        content_frame.pack(expand=True)
        
        # Symbol
        symbol_label = tk.Label(content_frame, 
                               text=symbol,
                               font=self.fonts['large_symbol'],
                               fg=self.colors['aether'],
                               bg=self.colors['void'])
        symbol_label.pack(pady=80)
        
        # Message
        message_label = tk.Label(content_frame, 
                                text=message + "\n\nThis feature is under development.",
                                font=self.fonts['subtitle'],
                                fg=self.colors['sage'],
                                bg=self.colors['void'],
                                justify='center')
        message_label.pack()
        
        self.screens[name] = screen

    def start_animations(self):
        """Start lightweight animations"""
        if self.animation_running:
            return
        self.animation_running = True
        self.animate_companion()
        self.animate_sparkles()

    def animate_companion(self):
        """Animate the floating companion"""
        try:
            if hasattr(self, 'companion') and self.current_screen == 'hub':
                # Cycle through companion states
                companions = ["🌟", "✨", "💫", "⭐"]
                current_index = getattr(self, 'companion_index', 0)
                
                self.companion.config(text=companions[current_index])
                self.companion_index = (current_index + 1) % len(companions)
            
            # Continue animation
            self.root.after(1200, self.animate_companion)
            
        except Exception as e:
            print(f"Companion animation error: {e}")
            self.root.after(2000, self.animate_companion)

    def animate_sparkles(self):
        """Animate background sparkles"""
        try:
            if hasattr(self, 'sparkles') and self.current_screen == 'hub':
                # Cycle sparkle opacity/visibility
                sparkle_states = ["✦", "✧", "✦", " "]
                current_state = getattr(self, 'sparkle_state', 0)
                
                for i, sparkle in enumerate(self.sparkles):
                    # Stagger sparkle animation
                    state_index = (current_state + i) % len(sparkle_states)
                    sparkle.config(text=sparkle_states[state_index])
                
                self.sparkle_state = (current_state + 1) % len(sparkle_states)
            
            # Continue animation
            self.root.after(1500, self.animate_sparkles)
            
        except Exception as e:
            print(f"Sparkle animation error: {e}")
            self.root.after(3000, self.animate_sparkles)

    def safe_navigate(self, screen_name):
        """Navigate with full error protection"""
        try:
            if screen_name in self.screens:
                self.show_screen(screen_name)
                print(f"✧ Navigated to {screen_name} ✧")
            else:
                print(f"Screen {screen_name} not found, returning to hub")
                self.show_screen('hub')
        except Exception as e:
            print(f"Navigation error: {e}")
            self.show_screen('hub')

    def show_screen(self, screen_name):
        """Switch between screens safely"""
        try:
            # Hide all screens
            for screen in self.screens.values():
                screen.pack_forget()
            
            # Show target screen
            if screen_name in self.screens:
                self.screens[screen_name].pack(fill='both', expand=True)
                self.current_screen = screen_name
            else:
                # Fallback to hub
                self.screens['hub'].pack(fill='both', expand=True)
                self.current_screen = 'hub'
                
        except Exception as e:
            print(f"Screen display error: {e}")

    def handle_click(self, event):
        """Handle all click events including exit gesture"""
        try:
            # Exit gesture: triple-tap top-left corner
            if event.x < 100 and event.y < 100:
                self.exit_taps += 1
                print(f"Exit tap {self.exit_taps}/3")
                if self.exit_taps >= 3:
                    self.graceful_exit()
                # Reset counter after 3 seconds
                self.root.after(3000, self.reset_exit_counter)
                
        except Exception as e:
            print(f"Click handler error: {e}")

    def reset_exit_counter(self):
        """Reset exit gesture counter"""
        self.exit_taps = 0

    def lighten_color(self, hex_color):
        """Create lighter version of color for hover effects"""
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lighter_rgb = tuple(min(255, int(c * 1.3)) for c in rgb)
            return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
        except:
            return hex_color

    def handle_error(self, context, error):
        """Universal error handler"""
        error_msg = f"Error in {context}: {str(error)}"
        print(f"🚨 {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")

    def graceful_exit(self):
        """Exit the application gracefully"""
        try:
            print("✧ Sacred journey ending gracefully ✧")
            self.animation_running = False
            if self.audio_enabled:
                pygame.mixer.quit()
            self.root.quit()
        except:
            print("✧ Force closing ✧")
            sys.exit(0)

    def run(self):
        """Start the sacred interface"""
        try:
            print("✧ Crumb UI v0.2 - Minimal Sacred Interface Starting ✧")
            print("Triple-tap top-left corner to exit")
            
            # Start main loop with error recovery
            while True:
                try:
                    self.root.mainloop()
                    break  # Normal exit
                except Exception as e:
                    self.handle_error("Main Loop", e)
                    # Try to recover
                    try:
                        self.root.update()
                    except:
                        break
                        
        except KeyboardInterrupt:
            print("\n✧ Sacred journey interrupted ✧")
        except Exception as e:
            self.handle_error("Application", e)
        finally:
            print("✧ Crumb UI session ended ✧")


def main():
    """Initialize and run Crumb with maximum reliability"""
    try:
        app = CrumbUI() 
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        print("✧ Application terminated ✧")


if __name__ == "__main__":
    main()
