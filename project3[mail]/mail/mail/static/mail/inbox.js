const inbox = "inbox";
const sent = "sent";
const archive = "archive";
const compose = "compose";

document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
  .querySelector("#inbox")
  .addEventListener("click", () => load_mailbox(inbox));
  document
  .querySelector("#sent")
  .addEventListener("click", () => load_mailbox(sent));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox(archive));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // Set what to do when the send form is submitted
  document.querySelector("#compose-form").onsubmit = send;

  // By default, load the inbox mailbox
  load_mailbox(inbox);
});

/**
 * Adds an email element to the current inbox view.
 *
 * @param element the email element to add
*/
function add_element(element) {
  document.querySelector("#emails-view").append(element);
}

/**
 * Clears all email elements in an inbox
*/
function clear_elements() {
  document.querySelector("#emails-view").innerHTML = "";
}

/**
 * Creates an html element to display an email in an inbox,
 * with an id, sender, subject, and date.
 */
function create_elements(id, sender, subject, date, read, mailbox) {
  let template = `
    <div class="email-box [[read]]">
      <span class="email-sender">${sender}</span>
      <span class="email-subject"><b>${subject}</b></span>
      <span class="email-date" style="float: right;">${date}</span>
    </div>`.replace("[[read]]", read ? "" : "unread");

  let email = document.createElement("div");
  email.innerHTML = template;
  email.addEventListener("click", () => load_email(id, mailbox));

  return email;
}

/**
 * Function to fetch the emails from a mailbox from the server.
 *
 * @param mailbox the mailbox to fetch emails from
 * @returns a Promise from fetching the emails. Use get_emails().then()
 * to access emails.
 */
function get_emails(mailbox) {
  return fetch(`/emails/${mailbox}`).then((response) => response.json());
}

/**
 * Takes the users data given to the compose form, and sends an email back
 * to the server using that data.
 */
function send() {
  // Get user data entered
  const recipients = document.querySelector("#recipients").value;
  const subject = document.querySelector("#subject").value;
  const body = document.querySelector("#body").value;

  // Log it for sanity sake
  console.log(
    `Sending email with data: recipients: ${recipients}, subject: ${subject}, body: ${body}`
  );

  // Send data to server
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => {
      response.json();
    })
    // Load sent mail page once sent
    .then((result) => {
      console.log("loading sent mail!");
      load_mailbox(sent);
    });

  // Return false so the page doesn't reload and load inbox instead of sent
  return false;
}

/**
 * Sets all nav button styles to the default unselected style
 */
function clear_button_styles() {
  buttons = [
    document.querySelector("#inbox"),
    document.querySelector("#sent"),
    document.querySelector("#archived"),
    document.querySelector("#compose"),
  ];

  for (const btn of buttons) {
    btn.classList.remove("btn-primary");
    btn.classList.add("btn-outline-primary");
  }
}

/**
 * Sets the given nav buttons style to show that it is active
 *
 * @param btn the active/pressed button to set the style of
 */
function set_button_active(btn) {
  const button = btn;
  button.classList.remove("btn-outline-primary");
  button.classList.add("btn-primary");
}

function compose_email() {
  // Set Nav Button Styles
  clear_button_styles();
  set_button_active(document.querySelector("#compose"));

  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#recipients").value = "";
  document.querySelector("#subject").value = "";
  document.querySelector("#body").value = "";
}

/**
 * Queries the server for a specific email (by ID),
 * and renders the response on the page.
 *
 * @param id the ID of the mail to load
 * @param mailbox the mailbox the email came from
 */

function load_email(id, mailbox) {
  // Show email view, and hide others
  document.querySelector("#email-view").style.display = "block";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Check if the email was sent by us
  let was_sent = false;
  if (mailbox === "sent") {
    was_sent = true;
  }

  // Mark email as being read, once we open it
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });

  // Get the email data from server, and render it in page
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      console.log(email);

      // Begin building the email view
      document.querySelector("#email-view").innerHTML = `
          <div><b>From:</b> ${email.sender}</div>
          <div><b>To:</b> ${email.recipients}</div>
          <div><b>Subject:</b> ${email.subject}</div>
          <div><b>Timestamp:</b> ${email.timestamp}</div>            
          
          <div class="email-buttons">
              <button class="btn-email" id="reply">Reply</button>
              <button class="btn-email" id="archive">${
                email["archived"] ? "Unarchive" : "Archive"
              }</button>
          </div>
          <hr>
          <div>
              ${email.body}
          </div>`;

      // Remove buttons if email was sent by us
      if (was_sent) {
        document.querySelector(".email-buttons").style.display = "none";
      }

      // Add archive button event listener
      document.querySelector("#archive").addEventListener("click", () => {
        fetch(`/emails/${id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: !email.archived,
          }),
        }).then((email) => {
          load_mailbox("inbox");
        });
      });

      // Add reply button event listener
      document.querySelector("#reply").addEventListener("click", () => {
        document.querySelector("#emails-view").style.display = "none";
        document.querySelector("#compose-view").style.display = "block";
        document.querySelector("#email-view").style.display = "none";

        document.querySelector("#recipients").value = email.sender;

        console.log(email.subject.slice(0, 3));
        console.log(email.subject.slice(0, 3) != "Re:");

        if (email.subject.slice(0, 3) != "Re:") {
          document.querySelector("#subject").value = "Re: " + email.subject;
        } else {
          document.querySelector("#subject").value = email.subject;
        }

        document.querySelector(
          "#body"
        ).value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n\n`;
      });
    });
}

/**
 * Loads and renders the emails from the given mailbox.
 *
 * @param mailbox the specific mailbox to load.
 */
function load_mailbox(mailbox) {
  console.log(`Loading mailbox: ${mailbox}`);
  //Set Nav Button Styles
  clear_button_styles();
  switch (mailbox) {
    case inbox:
      set_button_active(document.querySelector("#inbox"));
      break;
    case sent:
      set_button_active(document.querySelector("#sent"));
      break;
    case archive:
      set_button_active(document.querySelector("#archived"));
      break;
  }

  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";

  clear_elements();
  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  // Get emails from server, and render them in the inbox
  get_emails(mailbox).then((emails) => {
    console.log(`Loading emails for "${mailbox}"`);

    emails.forEach((email) => {
      add_element(
        create_elements(
          email.id,
          email.sender,
          email.subject,
          email.timestamp,
          email.read,
          mailbox
        )
      );
    });
  });
}
