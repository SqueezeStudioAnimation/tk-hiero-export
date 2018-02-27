from tank import Hook

class HieroGetShot(Hook):
    """
    Return a Shotgun Shot dictionary for the given Hiero items
    """
    def execute(self, item, data, **kwargs):
        """
        Takes a hiero.core.TrackItem as input and returns a data dictionary for
        the shot to update the cut info for.
        """
        # get the parent sequence for the Shot
        # (which in-turn has the parent episode)
        # sequence = self._get_sequence(item, data)

        # grab shot from Shotgun
        sg = self.parent.shotgun
        filt = [
            ["project", "is", self.parent.context.project],
            # ["sg_sequence", "is", sequence],
            ["code", "is", item.name()],
        ]
        fields = kwargs.get("fields", [])
        fields.append("sg_episode")
        shots = sg.find("Shot", filt, fields=fields)
        if len(shots) > 1:
            # can not handle multiple shots with the same name
            raise StandardError("Multiple shots named '%s' found", item.name())
        if len(shots) == 0:
            # create shot in shotgun
            shot_data = {
                "code": item.name(),
                # "sg_sequence": sequence,
                # "sg_episode": sequence['sg_episode'],
                "project": self.parent.context.project,
            }
            shot = sg.create("Shot", shot_data)
            self.parent.log_info("Created Shot in Shotgun: %s" % shot_data)
        else:
            shot = shots[0]

        # update the thumbnail for the shot
        self.parent.execute_hook(
            "hook_upload_thumbnail",
            entity=shot,
            source=item.source(),
            item=item,
            task=kwargs.get("task")
        )

        return shot

    # def _get_sequence(self, item, data):
    #     """Return the shotgun sequence for the given Hiero items"""
    #     # stick a lookup cache on the data object.
    #     if "seq_cache" not in data:
    #         data["seq_cache"] = {}
    #
    #     hiero_sequence = item.parentSequence()
    #     if hiero_sequence.guid() in data["seq_cache"]:
    #         return data["seq_cache"][hiero_sequence.guid()]
    #
    #     # sequence not found in cache, grab it from Shotgun
    #     sg = self.parent.shotgun
    #     filt = [
    #         ["project", "is", self.parent.context.project],
    #         ["code", "is", hiero_sequence.name()],
    #     ]
    #     fields = ['sg_episode']
    #     sequences = sg.find("Sequence", filt, fields)
    #     if len(sequences) > 1:
    #         # can not handle multiple sequences with the same name
    #         raise StandardError("Multiple sequences named '%s' found" % hiero_sequence.name())
    #
    #     if len(sequences) == 0:
    #         episode = self._get_episode(item, data)
    #         # create the sequence in shotgun
    #         seq_data = {
    #             "code": hiero_sequence.name(),
    #             "sg_episode": episode,
    #             "project": self.parent.context.project,
    #         }
    #         sequence = sg.create("Sequence", seq_data)
    #         self.parent.log_info("Created Sequence in Shotgun: %s" % seq_data)
    #     else:
    #         sequence = sequences[0]
    #
    #     # update the thumbnail for the sequence
    #     self.parent.execute_hook("hook_upload_thumbnail", entity=sequence, source=hiero_sequence, item=None)
    #
    #     # cache the results
    #     data["seq_cache"][hiero_sequence.guid()] = sequence
    #
    #     return sequence
    #
    # def _get_episode(self, item, data):
    #     """Return the shotgun episode for the given Hiero items.
    #     We define this as any tag linked to the sequence that starts
    #     with 'Ep'."""
    #     # We can get the episode by looking at the context
    #     if self.parent.context.entity['type'] == 'CustomEntity10':
    #         return self.parent.context.entity
    #
    #     # stick a lookup cache on the data object.
    #     if "epi_cache" not in data:
    #         data["epi_cache"] = {}
    #
    #     hiero_episode = None
    #     for t in item.parentSequence().tags():
    #         if t.name().startswith('E'):
    #             hiero_episode = t
    #             break
    #     if not hiero_episode:
    #         raise StandardError("No episode has been assigned to the sequence: " % item.parentSequence().name())
    #
    #     if hiero_episode.guid() in data["epi_cache"]:
    #         return data["epi_cache"][hiero_episode.guid()]
    #
    #     # episode not found in cache, grab it from Shotgun
    #     sg = self.parent.shotgun
    #     filt = [
    #         ["project", "is", self.parent.context.project],
    #         ["code", "is", hiero_episode.name()],
    #     ]
    #     episodes = sg.find("CustomEntity10", filt)
    #     if len(episodes) > 1:
    #         # can not handle multiple sequences with the same name
    #         raise StandardError("Multiple episodes named '%s' found" % hiero_episode.name())
    #
    #     if len(episodes) == 0:
    #         # create the sequence in shotgun
    #         epi_data = {
    #             "code": hiero_episode.name(),
    #             "project": self.parent.context.project,
    #         }
    #         episode = sg.create("CustomEntity10", epi_data)
    #         self.parent.log_info("Created Episode in Shotgun: %s" % epi_data)
    #     else:
    #         episode = episodes[0]
    #
    #     # cache the results
    #     data["epi_cache"][hiero_episode.guid()] = episode
    #
    #     return episode