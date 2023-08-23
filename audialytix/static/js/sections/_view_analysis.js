const handleChannelChange = (value) => {};

const setupCard = (data) => {
    $('#file-name').text(data.name);
    $('#file-author').text(data.author);

    if (data.analysis_type === 'stereo') {
        $('.ui.dropdown.channel').dropdown({
            values: [
                {
                    name: 'Left',
                    value: 'left',
                    selected: true,
                },
                {
                    name: 'Right',
                    value: 'right',
                },
            ],
            onChange: handleChannelChange,
        });
    } else {
        $('.ui.dropdown.channel')
            .dropdown({
                values: [
                    {
                        name: 'Mono',
                        value: 'mono',
                        selected: true,
                    },
                ],
            })
            .addClass('disabled');
    }
};

const setup = () => {
    fetch(`/api/info/${id}`)
        .then((res) => {
            return res.json();
        })
        .then((json) => {
            setupCard(json);
            $('#loader').hide();
            $('#analysis-card').show();
        });
};

$(setup);
