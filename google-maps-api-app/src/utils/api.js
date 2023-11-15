const API_KEY = 'AIzaSyAdqdhHkCtUiKxKAM4L9u8jGA8c4oBJu9Q'; //process.env.REACT_APP_GOOGLE_MAPS_API_KEY;

export const fetchPlaces = async (query) => {
    try {
        const geolocation = await getUserLocation();
        const url = new URL('https://maps.googleapis.com/maps/api/place/nearbysearch/json');
        url.search = new URLSearchParams({
            key: API_KEY,
            location: `${geolocation.lat},${geolocation.lng}`,
            radius: '8047', // 5 miles in meters
            keyword: query,
            rankby: 'prominence',
            type: 'establishment',
        });

        const response = await fetch(url);
        console.log(`Request URL: ${url}`);
        console.log(`Geolocation: Lat: ${geolocation.lat}, Lng: ${geolocation.lng}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('API response data:', data);  // Log the response data
        if (data.error_message) {
            throw new Error(data.error_message);
        }
        return data.results.filter(place => place.rating >= 4); // Assuming you want places with a rating of 4 and above
    } catch (error) {
        console.error("Error fetching places:", error);
        throw error; // Re-throw the error to be handled by the calling function
    }
};

export const getUserLocation = () => {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                });
            },
            (error) => {
                console.error("Error getting user location:", error);
                reject(error);
            },
            {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0,
            }
        );
    });
};

export const fetchDirections = (origin, destination, setDirections) => {
    const directionsService = new window.google.maps.DirectionsService();
    directionsService.route(
        {
            origin: origin,
            destination: destination,
            travelMode: window.google.maps.TravelMode.DRIVING,
        },
        (result, status) => {
            if (status === window.google.maps.DirectionsStatus.OK) {
                setDirections(result);
            } else {
                console.error(`error fetching directions ${result}`);
            }
        }
    );
};
