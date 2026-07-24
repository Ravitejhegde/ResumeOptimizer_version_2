import api from "../api/client";

export const uploadResume = async(file:File)=>{

    const form=new FormData();

    form.append("file",file);

    const response=await api.post(

        "/resume/upload",

        form,

        {

            headers:{

                "Content-Type":"multipart/form-data"

            }

        }

    );

    return response.data;

}