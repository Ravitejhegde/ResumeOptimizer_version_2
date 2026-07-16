type Props = {

    title: string;

    skills: string[];

};

export default function SkillList({

    title,
    skills,

}: Props) {

    return (

        <div className="skill-section">

            <h3>

                {title}

            </h3>

            {

                skills.length === 0

                ?

                <p>

                    None

                </p>

                :

                <ul>

                    {

                        skills.map((skill) => (

                            <li key={skill}>

                                {skill}

                            </li>

                        ))

                    }

                </ul>

            }

        </div>

    );

}