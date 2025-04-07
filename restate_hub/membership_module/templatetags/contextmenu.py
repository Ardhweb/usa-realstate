from django import template

register = template.Library()

@register.filter
def disable_contextmenu_click():
    return """<script>
        document.addEventListener("DOMContentLoaded", function() {
            document.addEventListener("contextmenu", function(event) {
                event.preventDefault();
            });
        });
    </script>"""
