<html>
  <head>
    <link rel="stylesheet" type="text/css" href="index.css"/>
  </head>

  <body>
    <div class="blue-square-container">

      <h1>Parliament agenda</h1>

      <?php
        $email = htmlspecialchars($_POST['email']);
        #echo $email;

        if(isset($_POST)){
          $output = shell_exec("python data_email/emailwhatson.py $email");
          echo "<h2>Email successfully sent to " . $email . ".</h2>";
          echo "<h2><a href='index.php'>Send another email?</a></h2>";
        }
        else{
          echo "Email failed to send.";
        }
      ?>

    </div>
  </body>
</html>
