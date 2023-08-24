const selected = {
    chartId: -1,
};

const zoomIn = () => {
    const currentZoom = $('#chart-area').css('width');
    const newZoom =
        Number(currentZoom.substr(0, currentZoom.length - 2)) + 250;
    $('#chart-area').css('width', `${newZoom}px`);
};

const zoomOut = () => {
    const currentZoom = $('#chart-area').css('width');
    const newZoom =
        Number(currentZoom.substr(0, currentZoom.length - 2)) - 250;
    $('#chart-area').css('width', `${newZoom}px`);
};

const getChartData = async (channel, analysis) => {
    res = await fetch(`/api/analysis/${id}/${channel}/${analysis}`);
    return await res.json();
};

const loadChart = () => {
    Chart.instances[selected.chartId]?.destroy();
    selected.chartId += 1;

    $('#chart-card').addClass('loading');

    getChartData(selected.channel, selected.analysis)
        .then((data) => {
            // TODO(Callum): Make this use the sample rate of the file
            const sampleRate = 44100 / 512;

            const ctx = $('canvas')[0].getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [...data.keys()].map(
                        (x) =>
                            Math.round(
                                (x / sampleRate + Number.EPSILON) * 100,
                            ) / 100,
                    ),
                    datasets: [
                        {
                            label: selected.analysis,
                            data: data,
                            borderColor: '#010c80',
                            backgroundColor: '#010c80',
                            borderWidth: 1,
                        },
                    ],
                },
                options: {
                    animation: false,
                    elements: {
                        point: {
                            radius: 0,
                            responsive: false,
                        },
                        scales: {
                            x: {
                                ticks: {
                                    sampleSize: sampleRate,
                                },
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                    },
                    maintainAspectRatio: false,
                },
            });
        })
        .then(() => $('#chart-card').removeClass('loading'));
};

const handleAnalysisChange = (e) => {
    if (selected.analysis === e.target.value) {
        return;
    }
    selected.analysis = e.target.value;
    loadChart();
};

const handleChannelChange = (value) => {
    selected.channel = value;
    loadChart();
};

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

        selected.channel = 'left';
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

        selected.channel = 'mono';
    }

    if (data.analysis_items.includes('onset')) {
        const complex = $(`<button class="ui button"></button>`)
            .text('Onset Complex')
            .val('onset.complex');
        const hfc = $(`<button class="ui button"></button>`)
            .text('Onset HFC')
            .val('onset.hfc');
        $('#analysis-buttons').append(complex, hfc);

        selected.analysis = 'onset.complex';
    }

    if (data.analysis_items.includes('spectral')) {
        const complexity = $(`<button class="ui button"></button>`)
            .text('Spectral Complexity')
            .val('spectral.complexity');
        $('#analysis-buttons').append(complexity);

        if (!selected.analysis) {
            selected.analysis = 'spectral.complexity';
        }
    }

    $('#analysis-buttons').children().click(handleAnalysisChange);

    loadChart();
};

const setup = () => {
    $('#zoom-in').click(zoomIn);
    $('#zoom-out').click(zoomOut);

    fetch(`/api/info/${id}`)
        .then((res) => {
            return res.json();
        })
        .then((json) => {
            setupCard(json);
            $('#loader').hide();
            $('#analysis-view').removeClass('hidden');
        });
};

$(setup);
