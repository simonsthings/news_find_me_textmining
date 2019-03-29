import React from "react";
import PropTypes from "prop-types";
import Keyword from "../../components/keywordChip";
//const Keyword = lazy(() => import("../../components/keywordChip"));

class KeyWordChipGroup extends React.Component {
  handleDeleteChip = () => index => {
    if (typeof this.props.handleDelete === "function") {
      return index;
    }
  };

  renderChips = () => {
    const { keywordObj } = this.props;
    if (!keywordObj) return;
    return keywordObj.map((word, i) => {
      return (
        <Keyword key={i} label={word} handleDelete={this.handleDeleteChip(i)} />
      );
    });
  };

  render() {
    return <>{this.renderChips()}</>;
  }
}

KeyWordChipGroup.propTypes = {
  keywordObj: PropTypes.array,
  handleDelete: PropTypes.func
};

export default KeyWordChipGroup;
