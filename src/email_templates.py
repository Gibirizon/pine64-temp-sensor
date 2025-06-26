PLAIN_TEXT_TEMPLATE = """\
TEMPERATURE ALERT

The temperature has dropped to {temperature}°C, which is below the warning threshold.

Please take appropriate action immediately.

This is an automated message from your temperature monitoring system.
"""

HTML_TEMPLATE = """\
<html>
  <head>
    <style>
      .alert {{
        color: #721c24;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
      }}
      .temperature {{
        font-size: 24px;
        font-weight: bold;
        color: #0056b3;
      }}
    </style>
  </head>
  <body>
    <h2>⚠️ Temperature Alert</h2>
    <div class="alert">
      <p>The current temperature has dropped to 
        <span class="temperature">{temperature}°C</span>
      </p>
      <p>This is below the warning threshold and requires immediate attention.</p>
    </div>
    <hr>
    <p><small>This is an automated message from your temperature monitoring system.</small></p>
  </body>
</html>
"""
