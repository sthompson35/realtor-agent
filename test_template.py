import jinja2

# Test if the analytics template can be parsed
try:
    with open('web/templates/analytics.html', 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Try to parse the template
    env = jinja2.Environment()
    template = env.from_string(template_content)

    print('✅ Analytics template syntax is valid')

    # Check for common issues
    if '{% extends' in template_content and 'base.html' in template_content:
        print('✅ Template extends base.html correctly')
    else:
        print('❌ Template extension issue')

    if '{% block content %}' in template_content and '{% endblock %}' in template_content:
        print('✅ Template has content block')
    else:
        print('❌ Missing content block')

except jinja2.TemplateSyntaxError as e:
    print(f'❌ Template syntax error: {e}')
    print(f'Line {e.lineno}: {e.message}')
except Exception as e:
    print(f'❌ Template parsing error: {e}')