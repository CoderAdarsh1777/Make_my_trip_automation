
class common:

    def __init__(self, driver):
          self.driver = driver

    def remove_overlays(self):
            self.driver.execute_script("""
                const elements = document.querySelectorAll('*');
                elements.forEach(e => {
                    const style = window.getComputedStyle(e);
                    if (
                        (style.position === 'fixed' || style.position === 'sticky' || style.position === 'absolute') &&
                        parseInt(style.zIndex) > 100
                    ) {
                        e.remove();
                    }
                });
            """)

    def remove_all_blockers(self):
        self.driver.execute_script("""
            const all = document.querySelectorAll('*');
            all.forEach(e => {
                const s = getComputedStyle(e);

                const z = parseInt(s.zIndex);
                const pos = s.position;

                // Remove anything high on screen
                if (!isNaN(z) && z > 10) {
                    e.remove();
                }

                // Remove any fixed/sticky banners
                if (['fixed','sticky','absolute'].includes(pos) && z >= 1) {
                    e.remove();
                }

                // Remove image slider (MakeMyTrip specific)
                if (e.className && e.className.toString().includes('imageSlideContainer')) {
                    e.remove();
                }
            });
        """)
