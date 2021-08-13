// you should copy and paste each generator seperately
[
    '{{repeat(4)}}',
    {
        model: "src.subject",
        id: '{{index(1)}}',
        fields: {
            name: "subject {{index(1)}}"
        }
    },


    '{{repeat(30)}}',
    {
        model: "src.question",
        id: '{{index(1)}}',
        fields: {
            subject: '{{integer(1,4)}}',
            text: 'Question {{index(1)}}',
            op1: "option 1",
            op2: "option 2",
            op3: "option 3",
            op4: "option 4",
            test_answer: '{{integer(1,4)}}'
        }
    },

]