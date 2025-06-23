
document.addEventListener("DOMContentLoaded", function()
{
  // Get URL
  const pathname = window.location.pathname;

  // Pseudo-tokenize
  const pathParts = pathname.split('/');

  // Get path after first /
  const tab = pathParts[1];

  // Testing
  console.log('Current Tab:', tab);

  // Initialize variable to hold tab
  let sidebarButton;

  // Check which tab
  if (tab === 'add_project')
  {
    sidebarButton = document.getElementById('add_project-btn');
    // console.log('You are on the Add Project tab');
  } 
  else if (tab === 'my_projects')
  {
    const tab2 = pathParts[2];
    console.log(tab2)
    if (!tab2)
    {
      sidebarButton = document.getElementById('my_projects-btn');
    }
    // console.log('You are on the Existing Project tab');
  } 
  else if (tab === 'users')
  {
    sidebarButton = document.getElementById('users-btn');
    // console.log('You are on the Users tab');
  } else if (tab === 'inbox')
  {
    sidebarButton = document.getElementById('inbox-btn');
    // console.log('You are on the Inbox tab');
  } else if (tab === 'myProfile')
  {
    sidebarButton = document.getElementById('myProfile-btn');
    // console.log('You are on the myProfile tab');
  } 
  else
  {
    sidebarButton = document.getElementById('explore-btn');
    // console.log('You are on the Explore tab');
  }

  // Disable button
  if (sidebarButton)
  {
    // sidebarButton.classList.add('disabled');
    sidebarButton.classList.remove('btn-sidebar');
    sidebarButton.classList.add('btn-sidebar-disabled');
    sidebarButton.setAttribute('aria-disabled', 'true');
    sidebarButton.setAttribute('tabindex', '-1');
    sidebarButton.setAttribute('href', '#');
  }

});
