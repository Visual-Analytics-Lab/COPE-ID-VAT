/*
    Navigation Button Toggle

    Included in index.html
    Toggles sidebar buttons
    Toggles my projects navigation buttons
*/

document.addEventListener("DOMContentLoaded", function()
{
  // Get URL
  const pathname = window.location.pathname;

  // Pseudo-tokenize
  const pathParts = pathname.split('/');

  // Get path after first /
  const pathPart1 = pathParts[1];

  // Testing
  console.log('Current Page:', pathPart1);

  // Initialize variable to hold page
  let sidebarButton;

  // Check which page
  if (pathPart1 === 'add_project')
  {
    sidebarButton = document.getElementById('add_project-btn');
    // console.log('You are on the Add Project page');
  } 
  else if (pathPart1 === 'my_projects')
  {
    const pathPart2 = pathParts[2];
    if (!pathPart2)
    {
      sidebarButton = document.getElementById('my_projects-btn');
    }
    else
    {
      // console.log(pathPart2);
      const myproject_path = document.getElementById(pathPart2);
      myproject_path.removeAttribute('href');
      myproject_path.classList.add('disabled');
    }
    // console.log('You are on the Existing Project page');
  } 
  else if (pathPart1 === 'users')
  {
    sidebarButton = document.getElementById('users-btn');
    // console.log('You are on the Users page');
  } else if (pathPart1 === 'inbox')
  {
    sidebarButton = document.getElementById('inbox-btn');
    // console.log('You are on the Inbox page');
  } else if (pathPart1 === 'myProfile')
  {
    sidebarButton = document.getElementById('myProfile-btn');
    // console.log('You are on the myProfile page');
  } 
  else
  {
    sidebarButton = document.getElementById('explore-btn');
    // console.log('You are on the Explore page');
  }

  // Disable button
  if (sidebarButton)
  {
    console.log(sidebarButton);
    sidebarButton.classList.remove('btn-sidebar');
    sidebarButton.classList.add('btn-sidebar-disabled');
    sidebarButton.setAttribute('aria-disabled', 'true');
    sidebarButton.setAttribute('tabindex', '-1');
    sidebarButton.setAttribute('href', '');
    sidebarButton.style.pointerEvents = 'none';
  }

});
