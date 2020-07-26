<html>
  <head>
    <link rel="stylesheet" type="text/css" href="index.css"/>
  </head>

  <body>
    <div class="blue-square-container">

      <h1>Parliament agenda</h1>

      <p><a href="#email-to-yourself">Email to yourself</a></p>

      <?php
      $output = shell_exec('data_web\webwhatson.py');
      echo $output;
      ?>

      <h2 id="email-to-yourself">Email to yourself</h2>

      <div class="add-new-word-form">
        <form action="email_sent.php" method="post">
          <label for="email">Email:</label><input type="text" name="email"><br><br>
          <input class="add-new-word-submit" type="submit" value="Send email">
        </form>
      </div>

    </div>
  </body>
</html>
