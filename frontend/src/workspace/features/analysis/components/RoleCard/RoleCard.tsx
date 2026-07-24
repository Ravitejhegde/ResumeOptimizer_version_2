import Card from "../../../../components/ui/Card/Card";

import styles from "./RoleCard.module.css";

import type { RoleCardProps } from "./RoleCard.types";

const RoleCard = ({
    role
}: RoleCardProps) => {

    return (

        <Card className={styles.card}>

            <span>

                Detected Role

            </span>

            <h4>

                {role}

            </h4>

        </Card>

    );

};

export default RoleCard;