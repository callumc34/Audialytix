const handleResponse = async (res) => {
    $('.ui.form').removeClass('loading');
    if (res.ok) return res.json();
    return Promise.reject(res);
};

const handleId = async (json) => {
    $('.ui.form').addClass('success');
    id = json.id;

    setTimeout(
        () => (window.location.href = `/analysis?id=${id}`),
        2000,
    );
};

const handleError = async (res) => {
    $('.ui.form').addClass('error');
};

const configureForm = () => {
    const form = $('.ui.form').form('get values');
    form.analysis_type = form.analysis_type === 'Stereo';
    form.onset = form.onset === 'on';
    form.spectral = form.spectral === 'on';

    const formData = new FormData();

    Object.entries(form).forEach(([key, value]) =>
        formData.append(key, value),
    );

    formData.append('file', $('#file-input')[0].files[0]);

    return formData;
};

const setupForm = () => {
    $('.ui.checkbox').checkbox();

    $('.selection.dropdown').dropdown();

    $('.ui.form').form({
        fields: {
            author: 'empty',
            name: 'empty',
            stereo: 'empty',
        },
    });

    $('.submit-button').click(() => {
        $('.ui.form').form('validate form');
        if ($('.ui.form').form('is valid')) {
            if (!$('#file-input').val()) {
                $('.ui.form').form('add errors', [
                    'Please select a file to upload.',
                ]);
                return;
            } else {
                $('.ui.form').addClass('loading');
                fetch('api/upload', {
                    method: 'POST',
                    body: configureForm(),
                })
                    .then(handleResponse)
                    .then(handleId)
                    .catch(handleError);
            }
        }
    });
};

$(setupForm);
