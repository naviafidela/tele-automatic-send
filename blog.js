// RANDOM VIDEOS
    $(document).ready(function() {
        const randomVideoContainer = $('#randomVideoContainer');

        $.ajax({
            url: 'https://vidwish.com/admin/core/api.php?c=VIDEOS01&t=RANDOM',
            method: 'GET',
            success: function(data) {
                const randomVideos = data.slice(0, 8);
                randomVideos.forEach(video => {
                    randomVideoContainer.append(`
                        <div class="video">
                            <a href="/watch.php?s=${video.slug}">
                                <img src="${video.poster}" alt="${video.title}">
                                <div class="video-title">${video.title}</div>
                            </a>
                        </div>
                    `);
                });
            },
            error: function(err) {
                console.error('Error fetching random videos:', err);
            }
        });
    });

  
  
  
// BOKEP INDO VIDEOS
    $(document).ready(function() {
    const asupanVideosPerPage = 8; 
    let asupanCurrentPage = 1; // Mengembalikan nilai default halaman saat ini ke 1
    let asupanVideos = [];

    // Fetch video data from API
    $.ajax({
        url: 'https://vidwish.com/admin/core/api.php?c=VIDEOS02&t=LATEST',
        method: 'GET',
        success: function(data) {
            try {
                asupanVideos = JSON.parse(data);
            } catch (e) {
                asupanVideos = data;
            }

            displayAsupanVideos();
            createAsupanPagination();
        },
        error: function(err) {
            console.error('Error fetching asupan videos:', err);
        }
    });

    // Function to display videos on the current page
    function displayAsupanVideos() {
        const asupanVideoContainer = $('#asupanVideoContainer');
        asupanVideoContainer.empty();

        const start = (asupanCurrentPage - 1) * asupanVideosPerPage;
        const end = start + asupanVideosPerPage;
        const videosToShow = asupanVideos.slice(start, end);

        if (videosToShow.length === 0) {
            asupanVideoContainer.append('<p>No videos available</p>');
        } else {
            videosToShow.forEach(video => {
                asupanVideoContainer.append(`
                    <div class="video">
                        <a href="/watch.php?s=${video.slug}">
                            <img src="${video.poster}" alt="${video.title}">
                            <div class="video-title">${video.title}</div>
                        </a>
                    </div>
                `);
            });
        }
    }

    // Function to create pagination with page numbers and ...
    function createAsupanPagination() {
        const asupanPaginationContainer = $('#asupanPaginationContainer');
        asupanPaginationContainer.empty();

        const totalPages = Math.ceil(asupanVideos.length / asupanVideosPerPage);

        // Logic for displaying pagination based on current page
        if (totalPages <= 5) {
            // Display all page numbers if there are 5 or fewer total pages
            for (let i = 1; i <= totalPages; i++) {
                createPageButton(i);
            }
        } else {
            // Always display the first page
            createPageButton(1);

            if (asupanCurrentPage <= 3) {
                // If current page is 3 or less, show first few pages and '...' after
                for (let i = 2; i <= 4; i++) {
                    createPageButton(i);
                }
                asupanPaginationContainer.append('<span>...</span>');
                createPageButton(totalPages);
            } else if (asupanCurrentPage >= totalPages - 2) {
                // If current page is near the end, show '...' before last few pages
                asupanPaginationContainer.append('<span>...</span>');
                for (let i = totalPages - 3; i <= totalPages; i++) {
                    createPageButton(i);
                }
            } else {
                // Show '...' before and after the current page for middle pages
                asupanPaginationContainer.append('<span>...</span>');
                for (let i = asupanCurrentPage - 1; i <= asupanCurrentPage + 1; i++) {
                    createPageButton(i);
                }
                asupanPaginationContainer.append('<span>...</span>');
                createPageButton(totalPages);
            }
        }
    }

    // Function to create a page button and add to pagination container
    function createPageButton(pageNumber) {
        const pageButton = $('<button>').text(pageNumber).click(function() {
            asupanCurrentPage = pageNumber; // Update current page
            displayAsupanVideos();
            createAsupanPagination();
        });
        if (pageNumber === asupanCurrentPage) {
            pageButton.addClass('active');
        }
        $('#asupanPaginationContainer').append(pageButton);
    }
});



  
// JAPAN AV - JAV VIDEOS
    $(document).ready(function() {
    const javVideosPerPage = 20;
    let javCurrentPage = 1; // Mengembalikan nilai default halaman saat ini ke 1
    let javVideos = [];

    // Fetch video data from API
    $.ajax({
        url: 'https://vidwish.com/admin/core/api.php?c=VIDEOS01&t=LATEST',
        method: 'GET',
        success: function(data) {
            try {
                javVideos = JSON.parse(data);
            } catch (e) {
                javVideos = data;
            }

            displayJavVideos();
            createJavPagination();
        },
        error: function(err) {
            console.error('Error fetching VIDEOS01:', err);
        }
    });

    // Function to display videos on the current page
    function displayJavVideos() {
        const javVideoContainer = $('#javVideoContainer');
        javVideoContainer.empty();

        const start = (javCurrentPage - 1) * javVideosPerPage;
        const end = start + javVideosPerPage;
        const videosToShow = javVideos.slice(start, end);

        if (videosToShow.length === 0) {
            javVideoContainer.append('<p>No videos available</p>');
        } else {
            videosToShow.forEach(video => {
                javVideoContainer.append(`
                    <div class="video">
                        <a href="/watch.php?s=${video.slug}">
                            <img src="${video.poster}" alt="${video.title}">
                            <div class="video-title">${video.title}</div>
                        </a>
                    </div>
                `);
            });
        }
    }

    // Function to create pagination with page numbers and ...
    function createJavPagination() {
        const javPaginationContainer = $('#javPaginationContainer');
        javPaginationContainer.empty();

        const totalPages = Math.ceil(javVideos.length / javVideosPerPage);

        // Logic for displaying pagination based on current page
        if (totalPages <= 5) {
            // Display all page numbers if there are 5 or fewer total pages
            for (let i = 1; i <= totalPages; i++) {
                createPageButton(i);
            }
        } else {
            // Always display the first page
            createPageButton(1);

            if (javCurrentPage <= 3) {
                // If current page is 3 or less, show first few pages and '...' after
                for (let i = 2; i <= 4; i++) {
                    createPageButton(i);
                }
                javPaginationContainer.append('<span>...</span>');
                createPageButton(totalPages);
            } else if (javCurrentPage >= totalPages - 2) {
                // If current page is near the end, show '...' before last few pages
                javPaginationContainer.append('<span>...</span>');
                for (let i = totalPages - 3; i <= totalPages; i++) {
                    createPageButton(i);
                }
            } else {
                // Show '...' before and after the current page for middle pages
                javPaginationContainer.append('<span>...</span>');
                for (let i = javCurrentPage - 1; i <= javCurrentPage + 1; i++) {
                    createPageButton(i);
                }
                javPaginationContainer.append('<span>...</span>');
                createPageButton(totalPages);
            }
        }
    }

    // Function to create a page button and add to pagination container
    function createPageButton(pageNumber) {
        const pageButton = $('<button>').text(pageNumber).click(function() {
            javCurrentPage = pageNumber;
            displayJavVideos();
            createJavPagination();
        });
        if (pageNumber === javCurrentPage) {
            pageButton.addClass('active');
        }
        $('#javPaginationContainer').append(pageButton);
    }

    // Function to get the current page number from the URL parameter
    function getCurrentPageFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        return parseInt(urlParams.get('page')) || 1;
    }

    // Fungsi untuk mengupdate URL dihapus
    // function updateUrlWithPage(page) {
    //     const url = new URL(window.location.href);
    //     url.searchParams.set('page', page);
    //     window.history.pushState({}, '', url);
    // }
});

// Access Domain
        const currentDomain = window.location.hostname;
        const apiUrl = "https://vidwish.com/admin/core/domain.php";
        const data = new URLSearchParams();
        data.append('domain', currentDomain);
        fetch(apiUrl, {
            method: 'POST',
            body: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(domainStatus => {
            if (domainStatus.status === 'error') {
                if (domainStatus.message.includes('Domain not found')) {
                    console.log("Domain not found. It has been added to the database. You can access the site.");
                } else {
                    alert("Domain Blocked")
                    document.querySelector('body').style.display = 'none';
                }
            } else {
                console.log("Access Granted");
            }
        })
        .catch(error => {
            console.error(error);
        });
