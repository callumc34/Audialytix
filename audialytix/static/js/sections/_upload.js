const configureForm = () => {
    const form = $('.ui.form').form('get values');
    form.stereo = form.stereo === 'Stereo';
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
            artist: 'empty',
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
                fetch('api/upload', {
                    method: 'POST',
                    body: configureForm(),
                });
            }
        }
    });
};

$(setupForm);
