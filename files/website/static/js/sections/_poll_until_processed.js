const checkStatus = () => {
    fetch(`/api/status/${id}`)
        .then((res) => {
            if (res.status === 200) {
                return res.json();
            } else {
                throw new Error(res.statusText);
            }
        })
        .then((json) => {
            if (json.status === 'failed') {
                throw new Error(json.message);
            } else if (json.status === 'fulfilled') {
                window.location.reload();
            }
        });
};

const setup = () => {
    setInterval(checkStatus, 1000);
};

$(setup);
